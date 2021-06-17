""" Sample of github repository creation. To be placed in routes/api.py
after all engineering issues have been resolved

Docs:
https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template-preview-notices
"""
# from flask import request
# from models.user import User
# from models.project import Project
from os import environ
from requests import post
from json import dumps

# @api.route('/create_repo', methods=['POST'], strict_slashes=False)
def create_repo():
    """ creates a new repository for a user based on a Makers-Club template """

    # user = User.get_by_id(request.form.get('user_id'))
    # project = Project.get_by_id(request.form.get('projet_id'))

    # TODO: change `users` db to include access_token; save these at sign-in
    access_token = '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' # user['access_token']
    template_repo = 'sample-template-repo' # project['name']
    headers = {
        'Authorization':f'token {access_token}',
        'Accept':'application/vnd.github.baptiste-preview+json' # !Github peculiarity-- see docs.
    }
    data = {
        'owner': 'thisathrowaway', # user['handle']
        'name':template_repo,
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

print(create_repo())
