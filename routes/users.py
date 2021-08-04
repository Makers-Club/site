from flask import render_template, request, g, redirect, url_for, abort
from os import environ
from routes import users
from models.user import User
from models.clients.maker_teams_client import MTClient

@users.route('/', methods=['GET'], strict_slashes=False)
def all():
    all_users = User.get_all(MTClient)
    current_user = request.current_user
    if current_user:
        current_user = current_user.to_dict()
    data = {
        'current_user': current_user,
        'users': all_users
    }
    return render_template('users.html', data=data)

@users.route('/<handle>', methods=['GET'], strict_slashes=False)
def profile(handle):
    current_user = request.current_user
    if current_user:
        current_user = current_user.to_dict()

    from models.clients.maker_teams_client import MTClient
    user = User.get_by_attribute_and_value(MTClient, 'handle', handle)

    if user is None:
        print(f"(routes/users:29)[Error: User is None]\n ... User w/ handle: {handle}\n ... Not Found or query failed")        
        abort(404)

    user = user.to_dict()

    data = {
        'current_user': current_user,
        'this_profile': user
    }
    return render_template('profile.html', data=data)

@users.route('/<handle>', methods=['POST'], strict_slashes=False)
def delete_user(handle):
    current_user = request.current_user
    if current_user:
        data = {
            'current_user': current_user.to_dict(),
        }
        if current_user.handle == handle:
            from models.clients.maker_teams_client import MTClient
            current_user.delete(MTClient)        
            msg = 'Your account has been deleted.'
            return redirect(url_for('landing.index', msg=msg))
    data = {}
    data['error'] = 'Not in my house.'
    return render_template('profile.html', data=data)
            
    

