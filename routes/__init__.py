from flask import Blueprint

landing = Blueprint('landing', __name__, url_prefix="")
auth = Blueprint('auth', __name__, url_prefix="/auth")
users = Blueprint('users', __name__, url_prefix="/users")
tutorial = Blueprint('tutorial', __name__, url_prefix="/tutorial")
projects = Blueprint('projects', __name__, url_prefix="/projects")
payments = Blueprint('payments', __name__, url_prefix="/payments")
api = Blueprint('api', __name__, url_prefix="/api")

from routes.landing import *
from routes.auth import *
from routes.users import *
from routes.tutorial import *
from routes.projects import *
from routes.payments import *
