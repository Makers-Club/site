"""Defines all methods and routes related to user authentication"""
from flask import request, render_template, Blueprint, abort, redirect, url_for, make_response
#from routes import auth
from routes import auth
from models.clients.auth.authorize import Authorize
from models.clients.maker_teams_client import MTClient
from models.clients.github_client import GithubClient
from models.clients.auth.github_authorization import GithubAuthorization as Github
from os import getenv


@auth.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    from models.session import Session
    cookie = request.cookies.get('session')
    user = Session.get_user_from_cookie(MTClient, cookie)
    if not user:
        return redirect(url_for('landing.index'))
    Session.delete_by_user_id(MTClient, user.id)
    return redirect(url_for('landing.index'))

@auth.route('/authorize_github_integration', methods=['GET'], strict_slashes=False)
def authorize_github_integration():
    """Sends user to Github Login to sign in."""
    return redirect(Authorize.integration(Github))


@auth.route('/github_callback', methods=['GET'], strict_slashes=False)
def github_callback():
    """ recieve a callback from github when users sign in or register """
    from models.user import User
    from models.clients.maker_teams_client import MTClient
    github_user_data = Github.user(request)
    user = User.get_by_id(MTClient, github_user_data.get('id'))
    if not user:
        user = User.create_new_user(MTClient, github_user_data)
    from models.clients.auth.authenticate import Authenticate
    session = Authenticate.login(user.access_token, user.id)
    if not session:
        print('***** NO SESSION')
        abort(500)
    #response = make_response(redirect(url_for('landing.presignup')))
    response = make_response(redirect(url_for('landing.index')))
    cookie = session.id
    response.set_cookie('session', cookie)
    return response
    