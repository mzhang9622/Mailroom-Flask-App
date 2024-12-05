'''
conftest.py
'''

import os
import pytest
import sys
from website import create_app
# sys.path.append(os.path.abspath(
# "/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App/website"))

sys.path.append('/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App')

@pytest.fixture
def test_client():
    """
    Test client fixture for simulating requests.
    """
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        yield test_client 
