from flask import jsonify, request
from requests import post
from routes import api
from os import environ
from models.auth import auth_client
from models.user import User

@api.route('/checker', methods=['POST'], strict_slashes=False)
def checker():
    response = post(environ['CHECKER_API_URL'], data=request.form)
    if response.status_code != 200:
        print('FAILURE: {}'.format(response.text))
        return jsonify({'checks': None})
    return jsonify({'checks': response.json()})