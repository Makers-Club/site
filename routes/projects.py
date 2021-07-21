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
    print(project_id, 'proj id')
    # Get the project that was just created with a template id
    #project = Project.get_by_id(MTClient, project_id)
    import requests
    project = requests.get('https://api.makerteams.org/projects/5b284552-e16b-4a99-a30f-53c6bf955416?token=123123').json()

    pts = ProjectTemplate.get_all(MTClient)
    project = {'some': 'data'}
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
        'repository_link': f'https://github.com/{current_user}/bws_directory',
        'roles': 'Facilitator Backend Frontend'
    }
    project = Project.create_new_project(MTClient, info.update(found))
    return render_template('project.html', data={'project': project.to_dict(), 'info': found})


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
    