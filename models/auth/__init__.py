from os import environ
from flask import url_for
from models.auth.github_client import GithubClient
from models.auth.auth import Auth

auth_data = {
    'client_id': environ['GITHUB_CLIENT_ID'],
    'client_secret': environ['GITHUB_CLIENT_SECRET'],
    # Russell, had to get rid of url_for because of a flask error. Feel free to
    # replicate it and debug it but it was beyond my flask-paygrade.
    # Sustainable long-term solution: environ['GITHUB_CALLBACK_URL']
    'redirect_uri': environ['GCP_DEV_URL'] + '/auth/github_callback'
}

gh_client = GithubClient(auth_data)
auth_client = Auth()