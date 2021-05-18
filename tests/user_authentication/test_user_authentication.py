from ..user_authentication import test_app
from pytest_bdd import scenario, given, when, then
import pytest
from main import test_app
from models.auth import Auth
from uuid import uuid4

@scenario('../features/user_authentication.feature', 'A new visitor signs in with github for the first time')
def test_yes():
    pass

fake_id = str(uuid4())

@pytest.fixture
@given('github sends an identity we haven\'t seen before')
def new_fake_user():
    user = Auth.get_user(fake_id)
    return user

@then('the user shouldn\'t match with our authentication')
def no_match(new_fake_user):
    assert new_fake_user is None

@when('a new user is created')
def new_user():
    Auth.register_user(fake_id, name="fakename", email="{}@email.com".format(fake_id), handle="fake{}".format(fake_id))

@then('the user should match with our authentication')
def user_matches_now():
    user = Auth.get_user(fake_id)
    assert user is not None # A user was found
    assert user.id == fake_id # and it was the right user