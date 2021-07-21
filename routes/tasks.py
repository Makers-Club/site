from flask import render_template, request
from routes import tasks
from models.auth import auth_client
from models.task import Task
from models.task_template import TaskTemplate
from models.clients.maker_teams_client import MTClient
from models.task_template import TaskTemplate

@tasks.route('/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index(id):
    tasks = Task.get_all(MTClient)
    task_dict = None
    for t in tasks:
        if t.id == id:
            task_dict = t.to_dict()
    infos = TaskTemplate.get_all(MTClient)
    info_dict = None
    for i in infos:
        print(i.id, task_dict.get('task_template_id'))
        if i.id == task_dict.get('task_template_id'):
            info_dict = i.to_dict()
            print(info_dict)
    data = {
        'task': task_dict,
        'current_user': request.current_user.to_dict(),
        'info': info_dict
    }
    return render_template('task.html', data=data)