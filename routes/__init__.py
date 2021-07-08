from flask import Blueprint

landing = Blueprint('landing', __name__, url_prefix="")
auth = Blueprint('auth', __name__, url_prefix="/auth")
users = Blueprint('users', __name__, url_prefix="/users")
projects = Blueprint('projects', __name__, url_prefix="/projects")
sprints = Blueprint('sprints', __name__, url_prefix="/sprints")
tasks = Blueprint('tasks', __name__, url_prefix="/tasks")
payments = Blueprint('payments', __name__, url_prefix="/payments")

from routes.landing import *
from routes.auth import *
from routes.users import *
from routes.projects import *
from routes.payments import *