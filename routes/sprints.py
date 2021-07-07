from flask import render_template, request
from routes import sprints
from models.auth import auth_client


@sprints.route('/<id>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def index(id):
    project = {'empt': 'sprint'}
    data = {
        'current_user': request.current_user.to_dict(),
        'sprint': 'no sprint here yet'
    }
    return render_template('project.html', data=data)