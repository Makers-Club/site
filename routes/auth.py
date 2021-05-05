"""Defines all methods and routes related to user authentication"""
from flask import request, render_template, Blueprint, abort, redirect, g
from requests import get, post # warning: deprecated
from os import environ
from re import search
from routes import auth


@auth.route('/auth', methods=['GET'], strict_slashes=False)
def get_gh_temporary_code():
    """Sends user to Github Login to sign in."""
    query_params = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'scope': 'user'
    }
    URL = 'https://github.com/login/oauth/authorize?'
    for key, value in query_params.items():
        URL += '{}={}&'.format(key, value)
    return redirect(URL)

@auth.route('/callback', methods=['GET'], strict_slashes=False)
def callback():
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

    email = get_user(gh_tmp_code)
    if email is None:
        # Future coders, address all edge cases! Check get_user() comments
        return 'No verified emails, buddy! Verify your GitHub email.'

    return render_template('dash.html', data={'authenticated_user': email})

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
    if gh_access_token is None:
        # either the code was fake or our Github credentials are off.
        return None
    user_data = get_gh_user_data(gh_access_token)
    if user_data is None:
        # I can't fathom when this would ever happen.
        return None
    # Later on this will be a User object, not a user email
    user_email = match_user(user_data)    
    return user_email

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
        'redirect_uri': environ['GCP_DEV_URL'] + 'callback'
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

    gh_response = get('https://api.github.com/user/emails', headers=headers)
    if gh_response.status_code != 200:
        return None
    
    return gh_response.json()

def match_user(user_data):
    """matches the user data returned by the Github API with our known users.
    
    Args:
        * user_data (list): The JSON response from the GitHub API call for the user's data.
                            As of now this is A LIST OF EMAIL DICTIONARIES.
    Return:
        * (str): Email as a string (FOR NOW)* Later it will be more user data
    """
    for emails_dict in user_data:
        if emails_dict.get('primary') and emails_dict.get('verified'):
            return emails_dict.get('email')
    
    return None