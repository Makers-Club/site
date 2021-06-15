from flask import jsonify, request
from requests import post
from routes import api
from os import environ
from pprint import pformat

@api.route('/checker', methods=['POST'], strict_slashes=False)
def checker():
    response = post(environ['CHECKER_API_URL'], data=request.form)
    if response.status_code != 200:
        print('FAILURE: {}'.format(response.text))
        return jsonify({'string': 'OUR CHECKER API IS DOWN'})
    return jsonify({'string': pformat(response.json())})
