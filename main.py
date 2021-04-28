from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import (CORS, cross_origin)
from os import environ
from uuid import uuid4
import requests
from routes import *

app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())

# Save these later elsewhere, Russ - J.I.
environ['GITHUB_CLIENT_ID'] = '25ea07bd2d607833d0bd'
environ['GITHUB_CLIENT_SECRET'] = '39da3ad6dfd757263026315bb3df8ad58da582a1'
home_url = 'https://8080-cs-1011683879296-default.cs-us-central1-mtyn.cloudshell.dev/'
    
CORS(app, resources=r"*")

app.register_blueprint(landing)

@app.route('/callback', methods=['GET'], strict_slashes=False)
def callback():

    # Data to pass to authentication url
    auth_data = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'client_secret': environ['GITHUB_CLIENT_SECRET'],
        'code': request.url.split('=')[1],
        'redirect_uri': home_url + 'callback'
        }
    auth_url = 'https://github.com/login/oauth/access_token?'
    response = requests.post(auth_url, auth_data)


    print(response.text)
    token = response.text.split('=')[1].split('&')[0]
    headers = {'content-type': 'application/json', 'Authorization': f'token {token}'}
    response = requests.get('https://api.github.com/user/emails', headers=headers)
    print(response.text)
    return redirect(url_for('landing.index'))


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



