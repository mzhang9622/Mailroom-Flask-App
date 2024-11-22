import pytest
from flask import url_for
from website import website, db, User
from models import Box
import sys

@pytest.fixture
def client():
    """
    Test client fixture for simulating HTTP requests.
    """
    website.config['TESTING'] = True
    website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    with website.test_client() as client:
        with website.app_context():
            db.create_all()  # Create tables for testing
        yield client

# @pytest.fixture
# def add_user():
#     """
#     Fixture to add a test user to the database.
#     """
#     def _add_user(email, password):
#         user = User(email=email)
#         user.set_password(password)  # Assuming a `set_password` method
#         with website.app_context():
#             db.session.add(user)
#             db.session.commit()
#     return _add_user


def test_login_success(client):
    # Simulate a POST request to /login with valid credentials
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Scan Box" in response.data

def test_invalid_email(client):
    # Simulate a POST request to /login with invalid email
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@bowdoin.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b"login-input-container" in response.data

def test_invalid_password(client):
    # Simulate a POST request to /login with invalid password
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': '123'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"login-input-container" in response.data


def test_logout_success(client):
    # Login so that logging out is possible
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    # Simulate the POST request to /logout
    response = client.post('/logout', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is redirected to the homepage
    assert b"MAILROOM" in response.data
    # Check if the user is not in admin homepage
    assert b"Delete Admin" not in response.data
    # Check if the user is logged out
    with client.session_transaction() as sess:
        # Check that there is no user in the session after logout
        assert '_user_id' not in sess

def test_logout_failure(client):

    client.post('/', follow_redirects=True)

    # Simulate the POST request to /logout while logged in
    response = client.post('/logout', follow_redirects=True)

    print(response.data.decode('utf-8'))

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"login-input-container" in response.data
    # Check if the user is not in admin homepage

def test_about_admin(client):
     # login as admin
    client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    response = client.get('/about', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"ABOUT THE MAILROOM" in response.data
    # Check if the user has the option to logout
    assert b"logout" in response.data


def test_about_non_admin(client):
    response = client.get('/about', follow_redirects=True)
    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"ABOUT THE MAILROOM" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data


#Broken because login button is wrong

def test_contact_admin(client):
     # login as admin
    client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    response = client.get('/contact', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is on the contact page
    assert b"gmail.com" in response.data
    # Check if the user has the option to logout
    assert b"logout" in response.data

def test_contact_non_admin(client):

    response = client.get('/contact', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"gmail.com" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data

def test_increase_box_admin(client):
    client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    with website.app_context():
        init_quan = Box.query.get(1).quantity
    response = client.post('/update_box/1', data={"quantity": 5}, follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).quantity == init_quan+5


    #Does not work because of overflow error

    # with website.app_context():
    #     init_quan = Box.query.get(1).quantity
    # response = client.post('/update_box/1', data={"quantity": sys.maxsize}, follow_redirects=True)
    # assert response.status_code == 200
    # with website.app_context():
    #     assert Box.query.get(1).quantity == init_quan+sys.maxsize


    # May or may not work, depends if check is built in or not

    # with website.app_context():
    #     init_quan = Box.query.get(1).quantity
    # response = client.post('/update_box/1', data={"quantity": 5.5}, follow_redirects=True)
    # assert response.status_code == 200
    # with website.app_context():
    #     assert Box.query.get(1).quantity == init_quan+5.5






# def test_contact_page(client):
#     response = client.get("/contact")
#     assert response.status_code == 200
#     assert b"access_key" in response.data  # Check if the access key is rendered in the template
