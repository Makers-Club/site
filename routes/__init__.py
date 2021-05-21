from flask import Blueprint

landing = Blueprint('landing', __name__, url_prefix="")
auth = Blueprint('auth', __name__, url_prefix="/auth")
users = Blueprint('users', __name__, url_prefix="/users")

from routes.landing import *
from routes.auth import *
from routes.users import *