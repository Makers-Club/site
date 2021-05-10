from main import client
from uuid import uuid4


TEST_USER_CREDENTIALS = str(uuid4())


def test_signup_should_return_status_code_200(client):
    data = {
        'email': TEST_USER_CREDENTIALS,
        'name': TEST_USER_CREDENTIALS,
        'username': TEST_USER_CREDENTIALS,
        'id': TEST_USER_CREDENTIALS,
        'token': TEST_USER_CREDENTIALS
    }
    response = client.post('/signup', data=data)
    assert(response.status_code == 200)


def test_signup_should_create_new_user(client):
    """
    Signup should result in a new user in our database.
    """
    from models.user import User
    new_user = User.get_by_id(TEST_USER_CREDENTIALS)
    assert(new_user)


def test_signup_should_also_login(client):
    """
    Signup should also log the new user into the site.
    """
    from models.auth import Session
    current_users_sessions = Session.get_by_user_id('')
    assert(TEST_USER_CREDENTIALS in current_users_sessions)

def test_login_should_gain_protected_access(client):
    """
    Login should allow users to view protected pages.
    """
    client.set_cookie('session', TEST_USER_CREDENTIALS)
    response = client.post('/account')
    assert(response.status_code == 200)


def test_login_should_create_new_session(client):
    """
    Login should create a new session in our database, associated with the logged in user.
    """

def test_logout_should_disable_protected_access(client):
    """
    Protected content should no longer be accessible after logout.
    """

def test_logout_should_delete_session(client):
    """
    Logout should delete the session created by login.
    """


"""
TO DO
protected content should not be viewable if not logged in
registration with incomplete user data should fail
login with incorrect or incomplete user data should fail
logout should succeed even if no matching session is found
logout should redirect to a public page
"""