from flask import render_template, request
from routes import sprints
from models.auth import auth_client
from models.sprint import Sprint
from models.sprint_template import SprintTemplate
from models.clients.maker_teams_client import MTClient
from models.task import Task


@sprints.route('/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index(id):
    sprints = Sprint.get_all(MTClient)
    sprint_dict = None
    for s in sprints:
        if s.id == id:
            sprint_dict = s.to_dict()
    infos = SprintTemplate.get_all(MTClient)
    info_dict = None
    for i in infos:
        if i.id == sprint_dict.get('sprint_template_id'):
            info_dict = i.to_dict()
    tasks = Task.get_all(MTClient)
    task_ids = []
    for t in tasks:
        if t.sprint_id == id:
            task_ids.append(t.id)
    sprint_dict['tasks'] = task_ids
    data = {
        'current_user': request.current_user.to_dict(),
        'sprint': sprint_dict,
        'info': info_dict
    }
    return render_template('sprint.html', data=data)