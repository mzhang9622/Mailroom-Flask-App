'''
website_test.py
'''

import sys
import sqlite3
import pytest
from website import website
from website import db
from models import Box
from models import User
#from flask import url_for
#from website import User

@pytest.fixture
def client():
    """
    Test client fixture for simulating requests.
    """
    website.config['TESTING'] = True
    website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    with website.test_client() as client:
        with website.app_context():
            db.create_all()  # Create tables for testing
        yield client


def test_login_success(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the main admin page
    '''
    # Simulate a POST request to /login with valid credentials
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Scan Box" in response.data

def test_invalid_email(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    # Simulate a POST request to /login with invalid email
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@bowdoin.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"login-input-container" in response.data

def test_invalid_password(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    # Simulate a POST request to /login with invalid password
    response = client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': '123'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"login-input-container" in response.data


def test_logout_success(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/logout' page is requested (POST)
    THEN: Check the user is taken to the non-admin home page
    '''
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
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/logout' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    client.post('/', follow_redirects=True)
    # Simulate the POST request to /logout while not logged in
    response = client.post('/logout', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically taken to the login page by flask
    assert b"login-input-container" in response.data
    # Check if the user is not in admin homepage

def test_about_admin(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/about' page is requested (GET)
    THEN: Check the user is taken to the admin's about page
    '''
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
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/about' page is requested (GET)
    THEN: Check the user is taken to the about page
    '''
    response = client.get('/about', follow_redirects=True)
    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"ABOUT THE MAILROOM" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data

def test_contact_admin(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/contact' page is requested (GET)
    THEN: Check the user is taken to the admin contact page
    '''
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
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/contact' page is requested (GET)
    THEN: Check the user is taken to the contact page
    '''
    response = client.get('/contact', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"gmail.com" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data

def test_increase_box_admin(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is increased by the specified amount
    '''
    client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #Does not work because database has been temporarily wiped
    with website.app_context():
        init_quan = Box.query.get(1).quantity
    response = client.post('/update_box/1', data={"quantity": 5}, follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).quantity == init_quan+5


    #Does not work because of overflow error
    with website.app_context():
        init_quan = Box.query.get(1).quantity
    response = client.post('/update_box/1', data={"quantity": sys.maxsize}, follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).quantity == init_quan+sys.maxsize


def test_decrease_box_admin(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is decreased by the specified amount
    '''
    client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #Does not work because database has been temporarily wiped
    with website.app_context():
        init_quan = Box.query.get(1).quantity
    response = client.post('/update_box/1', data={"quantity": -5}, follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).quantity == init_quan-5


    #Does not work because of overflow error
    with website.app_context():
        init_quan = Box.query.get(1).quantity
    response = client.post('/update_box/1', data={"quantity": -sys.maxsize}, follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).quantity == init_quan-sys.maxsize

def test_delete_box(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/delete_box/<int>' page is requested (POST)
    THEN: Check the box with the specified id is deleted
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    #Does not work because database has been temporarily wiped
    with website.app_context():
        init_name = Box.query.get(1).name
    response = client.post('/delete_box/1', follow_redirects=True)
    assert response.status_code == 200
    with website.app_context():
        assert Box.query.get(1).name != init_name

def test_delete_admin_success(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/delete_admin/<int>' page is requested (POST)
    THEN: Check the admin with the specified id is deleted
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    with website.app_context():
        init_email = User.query.get(1).email

    response = client.post('/delete_admin/1', follow_redirects=True)
    #Should be redirected to main.admin
    assert response.status_code == 302
    assert b"logout" in response.data
    assert b"Scan" in response.data

    with website.app_context():
        assert User.query.get(1).email != init_email


def test_delete_yourself_failure(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/delete_admin/<int>' page is requested (POST)
    THEN: Check that you cannot delete yourself
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    with website.app_context():
        init_email = User.query.get(1).email

    response = client.post('/delete_admin/1', follow_redirects=True)
    #Should be redirected to main.admin
    assert response.status_code == 302
    assert b"logout" in response.data
    assert b"Scan" in response.data

    #Verify Admin not deleted
    with website.app_context():
        assert User.query.get(1).email == init_email


def test_add_box(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/add_box' page is requested (POST)
    THEN: Check the box is added to the database
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    conn = sqlite3.connect('instance/maildatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM box")
    init_max = cursor.fetchone()[0]

    response = client.post('/add_box',
                data={
                'name': 'test',
                'quantity': 'test',
                'size': 'test',
                'link':  'test',
                'image':  'test',
                'low_stock':  'test',
                'barcode': 'test'
                },
            follow_redirects=True
        )

    #Should be redirected to main.admin
    assert response.status_code == 302
    assert b"logout" in response.data
    assert b"Scan" in response.data

    conn = sqlite3.connect('instance/maildatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM box")
    #Verify database now has one additional box
    assert cursor.fetchone()[0] == init_max + 1


def test_add_user_success(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/add_user' page is requested (POST)
    THEN: Check the user is added to the database
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    conn = sqlite3.connect('instance/maildatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM user")
    init_max = cursor.fetchone()[0]

    response = client.post('/add_user',
                data={
                #enter valid email
                'email': 'test@colby.edu',
                },
            follow_redirects=True
        )

    #Should be redirected to main.admin
    assert response.status_code == 302
    assert b"logout" in response.data
    assert b"Scan" in response.data

    conn = sqlite3.connect('instance/maildatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM user")
    #Verify database now has one additional user
    assert cursor.fetchone()[0] == init_max + 1


def test_admin_success(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/admin' page is requested (POST)
    THEN: Check the user is taken to the admin page
    '''
    client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = client.get('/admin', follow_redirects=True)

    #Should be taken to admin page
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Admin" in response.data


def test_admin_failure(client):
    '''
    GIVEN: A Flask app configured for testing with a test client
    WHEN: The '/admin' page is requested (POST)
    THEN: Check the user is not allowed on admin page
    '''
    #Should not work because not logged in
    response = client.get('/admin', follow_redirects=True)

    #Should be taken to non-admin home page
    assert response.status_code == 200
    assert b"login" in response.data
    assert b"Admin" not in response.data
