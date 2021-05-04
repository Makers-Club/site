from flask import Flask, jsonify, render_template, request, redirect, url_for, g
from flask_cors import (CORS, cross_origin)
from os import environ
from uuid import uuid4
from routes import *
from helpers import *
from models.engine import storage

app = Flask(__name__)
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
else:
    environ["FLASK_SECRET_KEY"] = str(uuid4())
CORS(app, resources={r"*": {"origins": "*"}})

app.register_blueprint(landing)
app.register_blueprint(auth)

"""
error handler functions
"""
@app.errorhandler(400)
def bad_request(error) -> str:
    """
    Bad request
    """
    return jsonify({"error": "Bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def Forbidden(error) -> str:
    """
    Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def Unauthorized(error) -> str:
    """
    Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
