from ..user_authentication import test_app
from pytest_bdd import scenario, given, when, then
import pytest

@scenario('../features/user_authentication.feature', 'User registers with their github identity')
def test_yea():
    pass

@pytest.fixture
@given('github confirms their identity')
def github_identity():
    from uuid import uuid4
    TEST_GITHUB_IDENTITY = str(uuid4())
    return TEST_GITHUB_IDENTITY

@then('the new user should exist in the database')
def new_user_exists(github_identity):
    from models.user import User
    assert(User.get_by_id(github_identity))