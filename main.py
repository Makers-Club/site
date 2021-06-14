from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from os import environ
import pytest
from uuid import uuid4
from functools import wraps
from routes import *
from flask import request, redirect, url_for

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
app.register_blueprint(users)
app.register_blueprint(tutorial)

@app.before_request
def before():
    for route in ['static/', 'favicon', 'auth/']:
        if route in request.url:
            return
    from models.auth import Auth
    logged_in_user = Auth.logged_in_user
    session = request.cookies.get('session')
    setattr(request, 'current_user', logged_in_user(session))


@app.route('/payment_successful', methods=['GET', 'POST'], strict_slashes=False)
def payment_successful():
    from models.charge import Charge
    import json
    json_str = request.data
    json_data = json.loads(json_str)
    price = json_data.get('data')
    if price:
        price = price.get('object')
        if price:
            price = price.get('amount')
    new_charge = Charge(price)
    new_charge.save()    
    print(new_charge.to_dict())
    return jsonify('success')


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
