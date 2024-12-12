'''
conftest.py
'''

import os
from website import create_app
from website import auth
from website import models
import sys
import pytest

sys.path.append(os.path.abspath(
    "/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App"))

print("")
print(sys.path)
print("")

# sys.path.append(os.path.abspath(
# "/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App/website"))

@pytest.fixture
def test_client():
    """
    Test client fixture for simulating requests.
    """
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        yield test_client

@pytest.fixture
def valid_test_user():
    '''
    Valid user
    '''
    user = models.User(email="jhsmit25@colby.edu")
    user.set_password("jordan")
    # db.session.add(user)
    # db.session.commit()
    return user

'''
Mocking the flow object for testing
'''
class MockFlow:
    def authorization_url(self):
        '''
        Authorization
        '''
        print("MockFlow.authorization_url() called")  # Debug output
        return "http://example.com/auth", "mock_state"

@pytest.fixture(scope='module')
def google_client():
    '''
    Google
    '''
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    if 'auth' not in flask_app.blueprints:
        flask_app.register_blueprint(auth.auth_blueprint)
    auth.flow = MockFlow()

    with flask_app.test_client() as test_client:
        yield test_client
