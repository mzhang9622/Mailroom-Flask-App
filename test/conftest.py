import os
import pytest
from website import create_app, db
from flask import session

@pytest.fixture
def test_client():
    """
    Test client fixture for simulating requests.
    """
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        yield test_client 
