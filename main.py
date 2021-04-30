from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import (CORS, cross_origin)
from os import environ
from uuid import uuid4
from re import search
import requests
from routes import *
from models.engine import storage

app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())
CORS(app, resources={r"*": {"origins": "*"}})

# Save these later elsewhere, Russ - J.I.
environ['GITHUB_CLIENT_ID'] = '25ea07bd2d607833d0bd'
environ['GITHUB_CLIENT_SECRET'] = '39da3ad6dfd757263026315bb3df8ad58da582a1'
home_url = 'https://8080-1f8078dd-2378-4707-8a3e-78d294857adf.cs-us-central1-mtyn.cloudshell.dev/'

app.register_blueprint(landing)


@app.route('/callback', methods=['GET'], strict_slashes=False)
def callback():
    """
    The Github OAuth API returns the user sign-in code to this redirect URL.
    This function:
        1. extracts the code and sends it back to the Github API to get an access token
           for the user's profile data
        2. re-pings the Github API with the access token to get the user's emails
        3. Checks the user emails to see if the user is known to us or not
            A. If we know the user, sign them in
            B. If we don't, sign them up
    """
    from models.user import User

    # Data to pass to authentication url
    auth_data = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'client_secret': environ['GITHUB_CLIENT_SECRET'],
        'code': request.args.get('code'),
        'redirect_uri': home_url + 'callback'
    }
    # The requests module is deprecated so we should change this at some point
    oauth_url = 'https://github.com/login/oauth/access_token?'
    response = requests.post(oauth_url, auth_data)

    # Preferably, we should be checking the value of response in case there are any errors.
    # Leaving some boiler plate here for now...
    # if response.status_code != 200:
    #     if response.status_code in [404, 400]:
    #         pass
    #     pass

    # Extract token from response query parameters using re.search
    token = search('access_token=(.*?)(&|$)', response.text)[1]
    headers = {
        'content-type': 'application/json',
        'Authorization': f'token {token}'
    }

    oauth_api_url = 'https://api.github.com/user/emails'
    response = requests.get(oauth_api_url, headers=headers)
    emails = response.json()
    data = {
        'primary_email': None,
        'other_emails': []
    }
    all_users = storage.all(User)
    user_emails = {user.email for user in all_users}
    for email_dict in emails:
        if email_dict['email'] in user_emails:
            return email_dict['email'] + " has signed in!"
        elif email_dict['verified'] == True:
            if email_dict['primary'] == True:
                data['primary_email'] = email_dict['email']
            else:
                data['other_emails'].append(email_dict['email'])

    if data['primary_email']:
        return 'First time seeing ya! Time to sign up!'

    return 'You have no *verified* emails with Github. Please verify your Github email address'


"""
error handler functions
"""


@app.errorhandler(400)
def bad_request(error) -> str:
    """
    Bad request
    """
    return jsonify({"error": "Bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def Forbidden(error) -> str:
    """
    Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """
    Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
