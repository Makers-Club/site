from os import environ, getenv
from flask import url_for
from models.auth.github_client import GithubClient
from models.auth.auth import Auth

auth_data = {
    'client_id': environ['GITHUB_CLIENT_ID'],
    'client_secret': environ['GITHUB_CLIENT_SECRET'],
    'redirect_uri': environ['GITHUB_CALLBACK_URL']
}
if getenv('PRODUCTION'):
    auth_data['redirect_uri'] = 'https://makerteams.org/auth/github_callback'
    
gh_client = GithubClient(auth_data)
auth_client = Auth()