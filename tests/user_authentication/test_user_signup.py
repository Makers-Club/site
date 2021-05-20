from main import test_app
from models.auth import Auth
from models.storage import DB
from models.user import User
import pytest
from pytest_bdd import scenario, given, when, then


register = Auth.register
dummy_user = User()


@scenario('../features/user_authentication.feature', 'User sign up')
def test_after_sign_up():
    dummy_user.delete()

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




# 2
# given they don't have the right info / we don't get it correctly from github - something like this
# when a user signs up
# they don't exist in the db
# they're told there was a github error



'''


Scenario: A logged in user visits the home page
Given the user was already logged in
When they visit the home page
Then they should be sent to their dashboard

Scenario: A visitor visits the homepage
Given the visitor is not signed in
When they visit the home page
Then they should see the landing page



Scenario: A visitor tries to access a non public page
Given the visitor is not logged in
When the user visits a non public page
Then they should be redirected to a signup page with a message

# logs out
# deletes account
# log out of all devices
'''
