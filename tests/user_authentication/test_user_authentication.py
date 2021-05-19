from models.auth import Auth
from models.storage import DB
from models.user import User
import pytest
from pytest_bdd import scenario, given, when, then




@scenario('../features/user_authentication.feature', 'User sign up')
def test_after():
    pass

register = Auth.register
dummy_user = User()

@pytest.fixture
@given('a user signs up')
def registered_user():
    return register(dummy_user)

@then('we should recognize them as one of our users')
def registered_user_is_in_database(registered_user):
    print(registered_user)
    user_in_database = User.get_by_id(registered_user.id)
    assert(registered_user == user_in_database)

# @then('they should be brought to their dashboard') - this is kind of like saying 'also this should happen'

    
# given they don't have the right info / we don't get it correctly from github - something like this
# when a user signs up
# they don't exist in the db
# they're told there was a github error