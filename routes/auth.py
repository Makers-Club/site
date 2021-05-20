"""Defines all methods and routes related to user authentication"""
from flask import request, render_template, Blueprint, abort, redirect, url_for
from requests import get, post # warning: deprecated
from os import environ
from re import search
from routes import auth
from main import login_required


class GithubClient():
    pass
    

@auth.route('/private')
@login_required
def private():
    return render_template('about.html', data=None)

@auth.route('/authenticate_with_github', methods=['GET'], strict_slashes=False)
def send_visitor_to_github():
    """Sends user to Github Login to sign in."""
    scopes = ['user', 'repo']
    query_params = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'scope': '%20'.join(scopes)
    }
    URL = 'https://github.com/login/oauth/authorize?'
    for key, value in query_params.items():
        URL += '{}={}&'.format(key, value)
    return redirect(URL)

@auth.route('/github_callback', methods=['GET'], strict_slashes=False)
def github_callback():
    """The Github sign-in redirects to this page with a temporary code in the
    query parameters. This function uses the code to get the user's profile
    information from Github to sign the user in.

    Return:
        * dash.html template or the correct error page
    """
    
    gh_tmp_code = request.args.get('code')
    if gh_tmp_code is None:
        # someone tried to access the naked URL, abort.
        abort(404)

    user, session = get_user(gh_tmp_code)
    if user is None:
        # Future coders, address all edge cases! Check get_user() comments
        return 'No verified emails, buddy! Verify your GitHub email.'
    from flask import make_response
    response = make_response(render_template('dash.html', data=user.to_dict()))
    response.set_cookie('session', session.id)
    return response

def get_user(gh_tmp_code):
    """Finds a user profile using Github OAuth temporary code.
    
    1. First we get_gh_access_token()
    2. Then we use gh_access_token to get_gh_user_data()
    3. Then we find a user that matches the data and return the user identifier (email)

    Args:
        * gh_tmp_code (str): code provided by GitHub callback used to request access token
    
    Return:
        * user_email (str): user identifier
    """
    
    gh_access_token = get_gh_access_token(gh_tmp_code)
    print(gh_access_token)
    if gh_access_token is None:
        # either the code was fake or our Github credentials are off.
        return None, None
    user_data = get_gh_user_data(gh_access_token)
    if user_data is None:
        # User has a Github account without any verified emails
        return None, None
    # we will redirect to /signup around here to separate github identity verification from registration
    # this way registration is can be tested with a test token.
    # Later on this will be a User object, not a user email
    user = match_user(user_data)    
    from models.auth import Auth
    session = Auth.login(gh_access_token, user.id)
    return user, session

def get_gh_access_token(gh_tmp_code):
    """Exchanges a temporary code for an access token from Github API
    
    Args:
        * gh_tmp_code (str): Github temporary sign-in code
    
    Return:
        * gh_access_token (str): Github access token or None on failure
    """

    # Make POST request to Github Login OAuth Access Token URL
    auth_data = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'client_secret': environ['GITHUB_CLIENT_SECRET'],
        'code': gh_tmp_code,
        'redirect_uri': environ['GCP_DEV_URL'] + url_for('auth.github_callback')
    }
    print(auth_data)
    oauth_url = 'https://github.com/login/oauth/access_token?'
    response = post(oauth_url, auth_data)

    # Find and return access token
    # See re.search docs if you don't understand what's going on here and have to.
    gh_access_token_match_object = search('access_token=(.*?)(&|$)', response.text)
    if gh_access_token_match_object is None:
        return None
    gh_access_token = gh_access_token_match_object[1]
    return gh_access_token

def get_gh_user_data(gh_access_token):
    """Uses a Github access token to retrieve user data

    Args:
        * gh_access_token (str): Github access token
    
    Return:
        * gh_response.json() (dict): Github user data as a dictionary
    """

    headers = {
        'content-type': 'application/json',
        'Authorization': f'token {gh_access_token}'
    }

    gh_response = get('https://api.github.com/user', headers=headers)
    if gh_response.status_code != 200:
        print('Faulty response')
        return None
    
    user_data = gh_response.json()
    if user_data['email'] is None: # if user email is private, GET /user/emails too
        gh_response = get('https://api.github.com/user/emails', headers=headers)
        for email_dict in gh_response.json():
            if email_dict.get('primary') and email_dict.get('verified'):
                user_data['email'] = email_dict.get('email')
                return user_data
        return None

    return user_data


def match_user(user_data):
    """matches the user data returned by the Github API with our known users.
    
    Args:
        * user_data (list): The JSON response from the GitHub API call for the user's data.
                            As of now this is A LIST OF EMAIL DICTIONARIES.
    Return:
        * (str): Email as a string (FOR NOW)* Later it will be more user data
    """
    user = None
    from models.user import User
    d = user_data
    user = User.get_by_id(d['id'])

    # No user? Make new user!
    if user is None:
        user = User(id=d['id'], email=d['email'], name=d['name'], handle=d['login'], avatar_url=d['avatar_url'])
        user.save()
        print('NEW USER {} ADDED TO DATABASE'.format(user.id))
    
    return user