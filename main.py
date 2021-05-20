from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from os import environ
import pytest
from uuid import uuid4
from functools import wraps
from routes import *
from flask import request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.current_user is None:
            return redirect(url_for('landing.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# initialize the app
app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())
CORS(app, resources={r"*": {"origins": "*"}})





@pytest.fixture
def test_app():
    """
    This is the test version of the app.
    It is imported by pytest unittests.
    We use this to make test requests.
    """
    # app.config['TESTING'] = True
    test_app = app.test_client()
    yield test_app


# register blueprints
app.register_blueprint(landing)
app.register_blueprint(auth)


@app.before_request
def before():
    from models.auth import Auth
    from flask import request
    from models.session import Session
    from uuid import uuid4
    logged_in_user = Auth.logged_in_user
    session = request.cookies.get('session')
    request.current_user = logged_in_user(session)
    print(request.current_user)


# handle errors (abort)
@app.errorhandler(400)
def bad_request(error) -> str:
    return jsonify({"error": "Bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(403)
def Forbidden(error) -> str:
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(401)
def Unauthorized(error) -> str:
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
