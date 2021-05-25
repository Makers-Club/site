from models.user import User
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
        user.save()
        return user
    
    @classmethod
    def login(cls, token, user_id):
        ''' log a user in '''
        from models.session import Session
        new_session = Session(token=token, user_id=user_id)
        new_session.save()
        return new_session
    
    @classmethod
    def logged_in_user(cls, session):
        from models.session import Session
        from models.user import User
        current_session = Session.get_by_id(session)
        if not current_session:
            return None
        user_id = current_session.user_id
        return User.get_by_id(user_id)
        

    