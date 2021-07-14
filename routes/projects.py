from flask import render_template, request, redirect, url_for
from routes import projects
from models.project import Project
from models.clients.maker_teams_client import MTClient
from models.auth import auth_client

@projects.route('/create/<template_id>', methods=['GET'], strict_slashes=False)
def create_project(template_id):
    print('template', template_id)
    project = Project.create_new_project(MTClient, {'project_template_id': template_id})    
    if not project:
        return redirect(url_for('landing.index'))
    return redirect(url_for('projects.index', template_id=template_id, project_id=project.id))


@projects.route('/<template_id>/<project_id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index(template_id, project_id):
    print(template_id, project_id)
    # Get the project that was just created with a template id
    project = Project.get_by_id(MTClient, project_id)
    
    found_template = None
    print(project.to_dict())
    

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
    