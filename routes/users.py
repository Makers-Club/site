from flask import render_template, request, g, redirect, url_for
from os import environ
from routes import users
from models.user import User
from models.auth import auth_client

@users.route('/', methods=['GET'], strict_slashes=False)
def all():
    all_users = User.get_all()
    current_user = request.current_user
    if current_user:
        current_user = current_user.to_dict()
    data = {
        'current_user': current_user,
        'users': all_users
    }
    return render_template('users.html', data=data)

@users.route('/<handle>', methods=['GET'], strict_slashes=False)
@auth_client.login_required
def profile(handle):
    current_user = request.current_user
    if current_user:
        current_user = current_user.to_dict()
    user = User.get_by_handle(handle)
    data = {
        'current_user': current_user,
        'user_profile': user.to_dict()
    }
    return render_template('profile.html', data=data)

@users.route('/<handle>', methods=['POST'], strict_slashes=False)
@auth_client.login_required
def delete_user(user_id):
    current_user = request.current_user.to_dict()
    data = {
        'current_user': current_user.to_dict(),
    }
    if current_user.handle != handle:
        data['error'] = 'Not in my house.'
        return render_template('profile.html', data=data)
    else:
        current_user.delete()        
        msg = 'Your account has been deleted.'
        return redirect(url_for('landing.index', msg=msg))

