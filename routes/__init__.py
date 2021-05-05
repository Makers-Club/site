from flask import Blueprint

landing = Blueprint('landing', __name__, url_prefix="")
auth = Blueprint('auth', __name__, url_prefix="")

from routes.landing import *
from routes.auth import *