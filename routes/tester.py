from flask import json, jsonify, request
from requests import post
from routes import tester
from os import environ
from models.auth import auth_client
from models.user import User

@tester.route('/', methods=['POST', 'GET'], strict_slashes=False)
def testing():
    response = post(environ['CHECKER_API_URL'], data=request.form)
    '''
    if response.status_code != 200:
        print('FAILURE: {}'.format(response.text))
        return jsonify({'checks': None})
    '''
    print(response.json())
    return 'ok'
    return jsonify({'checks': response.json()}) 
