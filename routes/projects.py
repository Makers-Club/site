from flask import render_template, request, redirect, url_for
from routes import projects
from models.project import Project
from models.project_template import ProjectTemplate
from models.clients.maker_teams_client import MTClient
from models.clients.auth.authenticate import Authenticate

auth_client = Authenticate()


@projects.route('/', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index():
    projects = Project.get_all(MTClient)
    if projects:
        projects = [p.to_dict() for p in projects]
    current_user = request.current_user.to_dict()
    data = {
        'projects': projects,
        'current_user': current_user
    }
    return render_template('all_projects.html', data=data)

@projects.route('/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def project(id):
    project = Project.get_by_id(MTClient, id)
    if project:
        project = project.to_dict()
    current_user = request.current_user.to_dict()
    from models.sprint import Sprint
    sprints = Sprint.get_all(MTClient)
    print(sprints, '****8')
    if sprints:
        sprints = [s.to_dict() for s in sprints]
    data = {
        'project': project,
        'current_user': current_user,
        'sprints': sprints
    }
    return render_template('project.html', data=data)
    



# CREATE_REPO HELPER TO BE PLACED IN SITE API
def create_repo(user, repo):
    """ creates a new repository for a user based on a Makers-Club template
    Docs:
    https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template-preview-notices
    """
    from json import dumps
    from requests import post
    access_token = user.access_token
    headers = {
        'Authorization':f'token {access_token}',
        'Accept':'application/vnd.github.baptiste-preview+json' # !Github peculiarity-- see docs.
    }
    data = {
        'owner': user.handle, # 'thisathrowaway',
        'name': repo,
        'description': 'description' # project['description']
        # !See github docs for other possible attributes
    }
    url = f'https://api.github.com/repos/Makers-Club/{repo}/generate'
    response = post(url, data=dumps(data), headers=headers)
    return response.status_code
    
'''
if response.status_code == 201: # Success
    return 'Success!'
if response.status_code == 422: # They already have a repo with same name
    return 'This repository already exists'
if response.status_code == 403: # "Forbidden"
    return 'We don\'t have permission to make a repo for you'
return 'Unknown error has occured'
'''
