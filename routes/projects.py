from flask import render_template, request, redirect, url_for
from routes import projects
from models.project import Project
from models.clients.maker_teams_client import MTClient
from models.auth import auth_client

@projects.route('/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index(id):
    projects = Project.get_all(MTClient)
    found_project = None
    for project in projects:
        if project.id == id:
            found_project = project
    print(found_project)
    if found_project:
        from models.project_template import ProjectTemplate
        project_infos = ProjectTemplate.get_all(MTClient)
        info = None
        for proj_info in project_infos:
            if proj_info.id == found_project.project_template_id:
                info = proj_info
                print(info.to_dict(), '*******\n')
        found_project = found_project.to_dict()
        print(found_project)
        
    data = {
        'current_user': request.current_user.to_dict(),
        'project': found_project,
        'info': info
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
    