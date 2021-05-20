from main import test_app
from models.auth import Auth
from models.storage import DB
from models.user import User
import pytest
from pytest_bdd import scenario, given, when, then
from uuid import uuid4


register = Auth.register
login = Auth.login
#login = Auth.login
dummy_user = User()


@scenario('../features/user_authentication.feature', 'User views non-public content')
def test_after_non_public_view():
    pass

@pytest.fixture
@given('a logged in user requests a non-public page')
def logged_in_response(test_app):
    registered_user = register(dummy_user)
    token = str(uuid4())
    logged_in_user = login(token, registered_user)
    test_app.set_cookie('localhost', 'session', '123')
    return test_app.get('/private').data.decode()


@then("they shouldn't get any errors or be redirected")
def response_is_good(logged_in_response):
    assert(logged_in_response.status_code == 200)