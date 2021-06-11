from flask import render_template, request
from routes import projects
from models.auth import auth_client

@projects.route('/', methods=['GET', 'POST'], strict_slashes=False)
@auth_client.login_required
def project():
    data = {
        'current_user': request.current_user,
        'name': 'Project "Hello, World!"',
        'repo': 'raw-discipline' 
    }
    return render_template('project.html', data=data)
