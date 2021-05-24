"""Defines all methods and routes related to user authentication"""
from flask import request, render_template, Blueprint, abort, redirect, url_for, make_response
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

@auth.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    from models.session import Session
    cookie = request.cookies.get('session')
    session = Session.get_by_id(cookie)
    if session:
        session.delete()
    return redirect(url_for('landing.index'))


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
    """What's our docstring policy"""
    
    gh_tmp_code = request.args.get('code')
    if gh_tmp_code is None:
        # someone tried to access the naked URL, abort.
        abort(404)

    user, session = get_user(gh_tmp_code)
    if user is None:
        # Future coders, address all edge cases! Check get_user() comments
        return 'No verified emails, buddy! Verify your GitHub email.'
    response = make_response(redirect('/'))
    response.set_cookie('session', session.id)
    return response

def get_user(gh_tmp_code):
    """receives github code, returns user and session"""
    
    gh_access_token = get_gh_access_token(gh_tmp_code)
    if gh_access_token is None:
        print('Github credentials are off or the code was fake')
        return None, None
    user_data = get_gh_user_data(gh_access_token)
    if user_data is None:
        # User has a Github account without any verified emails
        return None, None
    user = match_user(user_data)    
    from models.auth import Auth
    session = Auth.login(gh_access_token, user.id)
    return user, session

def get_gh_access_token(gh_tmp_code):
    """Exchanges a temporary code for an access token from Github API"""

    # Make POST request to Github Login OAuth Access Token URL
    auth_data = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'client_secret': environ['GITHUB_CLIENT_SECRET'],
        'code': gh_tmp_code,
        'redirect_uri': environ['GCP_DEV_URL'] + url_for('auth.github_callback')
    }
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
    """Uses a Github access token to retrieve user data"""

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
    """matches user data with a user, returns user"""
    from models.user import User
    d = user_data
    user = User.get_by_id(d['id'])

    # No user? Make new user!
    if user is None:
        user = User(id=d['id'], email=d['email'], name=d['name'], handle=d['login'], avatar_url=d['avatar_url'])
        user.save()
        print('NEW USER {} ADDED TO DATABASE'.format(user.id))
    
    return user