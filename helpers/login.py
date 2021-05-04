"""
Defines login()
"""
# The requests module is deprecated so we should change this at some point
from requests import get, post
from os import environ
from re import search

def login(code):
    """This function receives a Github OAuth user sign-in code, pings the Github API
    for an access token, re-pings the API for the user's data, and returns the user
    identifier (currently the user email)
    """
    auth_data = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'client_secret': environ['GITHUB_CLIENT_SECRET'],
        'code': code,
        'redirect_uri': environ['GCP_DEV_URL'] + 'callback'
    }
    oauth_url = 'https://github.com/login/oauth/access_token?'
    response = post(oauth_url, auth_data)
    if not response.text:
        # In future, this should have a more robust error-check
        return None

    # Extract token from response query parameters using re.search
    token = search('access_token=(.*?)(&|$)', response.text)[1]
    headers = {
        'content-type': 'application/json',
        'Authorization': f'token {token}'
    }

    response = get('https://api.github.com/user/emails', headers=headers)
    if response.status_code != 200:
        # In future, this should have a more robust error-check
        return None

    for emails_dict in response.json():
        if emails_dict.get('primary') and emails_dict.get('verified'):
            return emails_dict.get('email')

    return None
