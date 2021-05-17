from ..user_authentication import test_app
from pytest_bdd import scenario, given, when, then
import pytest
from main import test_app
from flask import url_for

@scenario('../features/user_authentication.feature', 'A visitor uses their github identity to registers as a user')
def test_yea():
    pass

@pytest.fixture
@given('github confirms the identity of a visitor')
def github_identity(test_app):
    from uuid import uuid4
    TEST_GITHUB_IDENTITY = str(uuid4())
    return TEST_GITHUB_IDENTITY

@when('we register a github identity as a new user')
def register_new_user(github_identity):
    from auth import register_user
    register_user(github_identity)

@then('a new user should exist in our database, based on the visitor identity')
def new_user_exists(github_identity):
    from models.user import User
    assert(User.get_by_id(github_identity))