'''
conftest.py
'''

import os
import pytest
import sys

sys.path.append(os.path.abspath(
    "/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App"))

print("")
print(sys.path)
print("")

from website import create_app
from website import auth
from website import models
from website import db
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
    user = models.User(email="jhsmit25@colby.edu")
    user.set_password("jordan")
    # db.session.add(user)
    # db.session.commit()
    return user
