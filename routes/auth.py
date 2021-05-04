"""Defines all routes related to user authentication"""
from flask import request, render_template, Blueprint, g
from helpers import *

auth = Blueprint('auth', __name__, url_prefix="")


@auth.route('/callback', methods=['GET'], strict_slashes=False)
def callback():
    email = login(request.args.get('code'))
    if email is None:
        return 'No verified emails, buddy! Verify your GitHub email.'
    return render_template('dash.html', data={'authenticated_user': email})
