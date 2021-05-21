from flask import render_template, request, g, redirect, url_for
from os import environ
from routes import users
from models.user import User

@users.route('/', methods=['GET'], strict_slashes=False)
def my_profile():
    """ render user profile template """
    data = set_user_data(request.current_user)
    if (data is not None):
        user_id = data.get('user_data').get('id')
        return redirect(url_for('users.user_by_id', user_id=user_id))
    else:
        return redirect(url_for('landing.index'))

@users.route('/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    # TODO: Use user_id in place of user_handle for time being
    user = User().get_by_id(user_id)
    data = set_user_data(user)

    return render_template('profile.html', data=data)

@users.route('/<user_id>', methods=['POST'], strict_slashes=False)
def delete_user_by_id(user_id):
    user = request.current_user.to_dict()
    if user.get('id') != user_id:
        return redirect( url_for('landing.index') )
    else:
        request.current_user.delete()
    return redirect(url_for('landing.index'))



def set_user_data(user=None):
    if user is None:
        return None
    data = {
        'authorized': user.to_dict()['id'] == request.current_user.to_dict()['id'],
        'user_data': {
            'handle': "",
            'id': "",
            'email': "",
            'avatar_url': "",
            'name': ""
        }
    }
    data['user_data'].update(user.to_dict())
    return data