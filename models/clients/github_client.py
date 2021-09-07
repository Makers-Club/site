from os import getenv
from flask import request
from models.clients.base_client import BaseClient


class GithubClient(BaseClient):
    
    credentials = {
        'client_id': getenv('GITHUB_CLIENT_ID'),
        'client_secret': getenv('GITHUB_CLIENT_SECRET'),
        'redirect_uri': getenv('GITHUB_CALLBACK_URL'),

        }
    if getenv('PRODUCTION'):
        credentials['redirect_uri'] = 'https://makerteams.org/auth/github_callback'
    url = 'https://github.com'

    @classmethod
    def authorization_token(cls, token_url, data):
        import requests
        from re import search
        response = requests.post(token_url, data=data)
        match = search('access_token=(.*?)(&|$)', response.text)
        if match is None:
            #print(response.text)
            #print(data)
            return None
        # match[0] is the full matched string ('access_token=...')
        # match[1] is the access token itself.
        return match[1]
