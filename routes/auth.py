"""Defines all methods and routes related to user authentication"""
from flask import request, render_template, Blueprint, abort, redirect, url_for, make_response
#from routes import auth
from routes import auth
from models.auth.auth import Auth
from models.auth import gh_client
from models.clients.maker_teams_client import MTClient
from os import environ



    
@auth.route('/private')
@Auth.login_required
def private():
    return render_template('about.html', data=None)

@auth.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    from models.session import Session
    cookie = request.cookies.get('session')
    user = Session.get_user_from_cookie(MTClient, cookie)
    if not user:
        return redirect(url_for('landing.index'))
    Session.delete_by_user_id(MTClient, user.id)
    return redirect(url_for('landing.index'))


@auth.route('/authenticate_with_github', methods=['GET'], strict_slashes=False)
def send_visitor_to_github():
    """Sends user to Github Login to sign in."""
    # lets put these credentials into githubclient as class variables
    scopes = ['read:user', 'user:email', 'public_repo']
    query_params = {
        'client_id': environ['GITHUB_CLIENT_ID'],
        'scope': '%20'.join(scopes)
    }
    URL = 'https://github.com/login/oauth/authorize?'
    for key, value in query_params.items():
        URL += '{}={}&'.format(key, value)
    return redirect(URL)

@auth.route('/github_callback', methods=['GET'], strict_slashes=False)
def github_callback():
    """What's our docstring policy"""
    
    gh_tmp_code = request.args.get('code')
    if gh_tmp_code is None:
        # someone tried to access the naked URL, abort.
        abort(404)

    user, session = gh_client.get_user(gh_tmp_code)
    print(user, session)
    if user is None:
        # See issues #18 and #28
        return 'No verified emails! Please verify your email with GitHub and try again.'
    # this was for deploying the pre-signup version of the landing page
    response = make_response(redirect(url_for('landing.presignup')))
    #response = make_response(redirect(url_for('landing.index')))
    response.set_cookie('session', session.id)
    return response


