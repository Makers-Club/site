from models.user import User
from models.clients.maker_teams_client import MTClient
from models.session import Session
from functools import wraps
from flask import request, redirect, url_for

class Auth:
    def __init__(self):
        pass

    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user') or not request.current_user:
                return redirect(url_for('auth.send_visitor_to_github', next=request.url))
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def register(cls, user):
        ''' register a new user '''
        if not type(user) == User:
            raise TypeError
        user = User.create_new_user(MTClient)
        return user
    
    @classmethod
    def login(cls, token, user_id):
        ''' log a user in '''
        from models.session import Session
        new_session = Session.create_new(MTClient, token, user_id)
        return new_session
    
    @classmethod
    def logged_in_user(cls, session):
        return Session.get_user_from_cookie(MTClient, session)
        

    