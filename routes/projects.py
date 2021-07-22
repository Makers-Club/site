from flask import render_template, request, redirect, url_for
from routes import projects
from models.project import Project
from models.project_template import ProjectTemplate
from models.clients.maker_teams_client import MTClient
from models.auth import auth_client


@projects.route('/', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index():
    projects = Project.get_all(MTClient)
    templates = ProjectTemplate.get_all(MTClient)
    if projects:
        projects = [obj.to_dict() for obj in projects]
    if templates:
        templates = [obj.to_dict() for obj in templates]
    current_user = request.current_user.to_dict()
    data = {
        'projects': projects,
        'templates': templates,
        'current_user': current_user
    }
    return render_template('all_projects.html', data=data)
    

@projects.route('/create/<template_id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def create_project(template_id):
    templates = ProjectTemplate.get_all(MTClient)
    cost = 0
    for template in templates:
        if template.id == template_id:
            cost = template.cost
    current_user = request.current_user
    if cost > current_user.credits:
        data = {'msg': 'Not enough credits.'}
        return redirect(url_for('landing.index'), data=data)
    project = Project.create_new_project(MTClient, {'project_template_id': template_id})  
    if not project:
        return redirect(url_for('landing.index'))
    updated_credits = current_user.credits - cost
    updated_user = current_user.update(MTClient, 'credits', updated_credits)
    if not updated_user:
        data = {'msg': "We're having trouble charging your credits. Please contact support."}
        return redirect(url_for('landing.index'), data=data)
    print(updated_user)
    return redirect(url_for('projects.one', template_id=template_id, project_id=project.id))


@projects.route('/<template_id>/<project_id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def one(template_id, project_id):
    from models.sprint import Sprint
    print(project_id, 'proj id')
    # Get the project that was just created with a template id
    project = Project.get_by_id(MTClient, project_id)
    if project:
        project = project.to_dict()
    pts = ProjectTemplate.get_all(MTClient)
    sprints = Sprint.get_all(MTClient)
    print(sprints)
    our_sprints = []
    for s in sprints:
        if s.project_id == project.get('id'):
            our_sprints.append(s.id)
    project['sprints'] = our_sprints
    data = {
        'current_user': request.current_user.to_dict(),
        'this_project': project,
        'project_info': {'test': 'yea'}
    }
    return render_template('project.html', data=data)

@projects.route('/unlock/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def unlock(id):
    from models.project_template import ProjectTemplate
    current_user = request.current_user
    all_templates = ProjectTemplate.get_all(MTClient)
    found = None
    for each in all_templates:
        if each.id == id:
            found = each.to_dict()
    if not found:
        return render_template('index.html', data={'msg': 'ERROR*****'})
    info = {
        'name': 'BWS Business Directory',
        'repository': 'sample-template-repo',
        'repository_link': f'https://github.com/{current_user}/sample-template-repo',
        'roles': 'Facilitator Backend Frontend'
    }
    project = Project.create_new_project(MTClient, info.update(found))
    # Create repository
    repo_status = create_repo(current_user, info['repository'])
    return render_template('project.html', data={'this_project': project.to_dict(), 'project_info': info, 'repo_status': repo_status})


@projects.route('/<id>/<sid>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def sprint(id, sid):
    from models.sprint_template import SprintTemplate
    from models.sprint import Sprint
    sprint_templates = SprintTemplate.get_all(MTClient)[0]
    sprint = Sprint.get_all(MTClient)[0]
    data = {
        'current_user': request.current_user.to_dict(),
        'sprint': sprint.to_dict(),
        'info': sprint_templates.to_dict()
    }
    return render_template('sprint.html', data=data)
    

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

    if response.status_code == 201: # Success
        return 'Success!'
    if response.status_code == 422: # They already have a repo with same name
        return 'This repository already exists'
    if response.status_code == 403: # "Forbidden"
        return 'We don\'t have permission to make a repo for you'
    return 'Unknown error has occured'
