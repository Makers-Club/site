from flask import jsonify, request
from requests import post
from routes import api
from os import environ
from models.auth import auth_client
from models.user import User
from json import dumps

@api.route('/checker', methods=['POST'], strict_slashes=False)
def checker():
    response = post(environ['CHECKER_API_URL'], data=request.form)
    if response.status_code != 200:
        print('FAILURE: {}'.format(response.text))
        return jsonify({'checks': None})
    return jsonify({'checks': response.json()})

@api.route('/create_repo', methods=['POST'], strict_slashes=False)
def create_repo():
    """ creates a new repository for a user based on a Makers-Club template
    
    Docs:
    https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template-preview-notices
    """

    user = User.get_by_id(request.form.get('user_id'))
    
    # project = Project.get_by_id(request.form.get('project_id'))

    access_token = user['access_token'] # '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'
    template_repo = 'hello-world' # project['name']
    headers = {
        'Authorization':f'token {access_token}',
        'Accept':'application/vnd.github.baptiste-preview+json' # !Github peculiarity-- see docs.
    }
    data = {
        'owner': user['handle'], # 'thisathrowaway',
        'name': template_repo,
        'description': 'description' # project['description']
        # !See github docs for other possible attributes
    }
    url = f'https://api.github.com/repos/Makers-Club/{template_repo}/generate'
    response = post(url, data=dumps(data), headers=headers)

    if response.status_code == 201: # Success
        return 'Success!'
    if response.status_code == 422: # They already have a repo with same name
        return 'This repository already exists'
    if response.status_code == 403: # "Forbidden"
        return 'We don\'t have permission to make a repo for you'
    return 'Unknown error has occured'
