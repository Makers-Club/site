from flask import Blueprint
from routes.auth import auth

landing = Blueprint('landing', __name__, url_prefix="")

from routes.landing import *