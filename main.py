from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from os import environ, getenv
from uuid import uuid4
from routes import *
from flask import request, redirect, url_for



# initialize the app
app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = getenv("FLASK_SECRET_KEY")
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())
CORS(app, resources={r"*": {"origins": "*"}})


# register blueprints
app.register_blueprint(landing)
app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(projects)
app.register_blueprint(payments)
app.register_blueprint(sprints)
app.register_blueprint(tasks)

@app.before_request
def before():
    for route in ['static/', 'favicon', 'auth/']:
        if route in request.url:
            return
    from models.auth.auth import Auth
    logged_in_user = Auth.logged_in_user
    session = request.cookies.get('session')
    setattr(request, 'current_user', logged_in_user(session))





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
