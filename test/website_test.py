'''
website_test.py
'''

import io
import random
import string
import sys
import sqlite3
import pytest

import sys
import os
sys.path.append(os.path.abspath("/Users/jordansmith/Desktop/CS321/group-sprint-2/Mailroom-Flask-App/website"))

from website import create_app, db
from website.models import Box, User
from werkzeug.security import generate_password_hash

# @pytest.fixture
# def client():
#     """
#     Test client fixture for simulating requests.
#     """
#     website.config['TESTING'] = True
#     website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
#     with website.test_client() as client:
#         with website.app_context():
#             db.create_all()  # Create tables for testing
#         yield client


def test_login_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the main admin page
    '''
    app = create_app()
    with app.app_context():
        if not User.query.filter_by(email = "jhsmit25@colby.edu").all():
            user = User(email = "jhsmit25@colby.edu", password_hash = generate_password_hash('jordan'))
            db.session.add(user)
            db.session.commit()


    # Simulate a POST request to /login with valid credentials    
    response = test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    print(response.data)
    assert response.status_code == 200
    assert b"Scan Box" in response.data

def test_invalid_email(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    # Simulate a POST request to /login with invalid email
    response = test_client.post(
        '/login',
        data={'email': 'jhsmit25@bowdoin.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"login-input-container" in response.data

def test_invalid_password(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    # Simulate a POST request to /login with invalid password
    response = test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': '123'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"login-input-container" in response.data


def test_logout_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/logout' page is requested (POST)
    THEN: Check the user is taken to the non-admin home page
    '''
    # Login so that logging out is possible
    response = test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    # Simulate the POST request to /logout
    response = test_client.post('/logout', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is redirected to the homepage
    assert b"MAILROOM" in response.data
    # Check if the user is not in admin homepage
    assert b"Delete Admin" not in response.data
    # Check if the user is logged out
    with test_client.session_transaction() as sess:
        # Check that there is no user in the session after logout
        assert '_user_id' not in sess

def test_logout_failure(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/logout' page is requested (POST)
    THEN: Check the user is taken to the login page
    '''
    test_client.post('/', follow_redirects=True)
    # Simulate the POST request to /logout while not logged in
    response = test_client.post('/logout', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically taken to the login page by flask
    assert b"login-input-container" in response.data
    # Check if the user is not in admin homepage

def test_about_admin(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/about' page is requested (GET)
    THEN: Check the user is taken to the admin's about page
    '''
     # login as admin
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    response = test_client.get('/about', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"ABOUT THE MAILROOM" in response.data
    # Check if the user has the option to logout
    assert b"logout" in response.data


def test_about_non_admin(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/about' page is requested (GET)
    THEN: Check the user is taken to the about page
    '''
    response = test_client.get('/about', follow_redirects=True)
    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"ABOUT THE MAILROOM" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data

def test_contact_admin(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/contact' page is requested (GET)
    THEN: Check the user is taken to the admin contact page
    '''
     # login as admin
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    response = test_client.get('/contact', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is on the contact page
    assert b"gmail.com" in response.data
    # Check if the user has the option to logout
    assert b"logout" in response.data

def test_contact_non_admin(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/contact' page is requested (GET)
    THEN: Check the user is taken to the contact page
    '''
    response = test_client.get('/contact', follow_redirects=True)

    assert response.status_code == 200
    # Check if the user is automatically redirected to the login page by flask
    assert b"gmail.com" in response.data
    # Check if the user has the option to login
    assert b"login" in response.data

def test_increase_box(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is increased by the specified amount
    '''
    app = create_app()
    with app.app_context():
        if not Box.query.filter_by(name = "test").all():
            name = "test"
            quantity = 5
            size = "test"
            link = "test"
            image = "mule"
            # image.save("static/images/" + image.filename)
            low_stock = 0
            barcode = "test"
            box = Box(id=1, name = name, quantity = quantity, size = size, link = link,
                    image = image, low_stock = low_stock, barcode = barcode)
            db.session.add(box)
            db.session.commit()
            print("WORKING")

    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #Does not work because database has been temporarily wiped
    with app.app_context():
        init_quan = Box.query.get(1).quantity
    response = test_client.post('/update_box/1', data={'quantity': '5'}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(1).quantity == init_quan+5


    #Check that system can handle overflow
    with app.app_context():
        init_quan = Box.query.get(1).quantity
    response = test_client.post('/update_box/1', data={"quantity": str(sys.maxsize)}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(1).quantity != init_quan+sys.maxsize


def test_decrease_box_admin(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is decreased by the specified amount
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #Does not work because database has been temporarily wiped
    app = create_app()
    with app.app_context():
        init_quan = Box.query.get(1).quantity
    response = test_client.post('/update_box/1', data={"quantity": "-5"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(1).quantity == init_quan-5


    #Check that system can handle overflow
    with app.app_context():
        init_quan = Box.query.get(1).quantity
    response = test_client.post('/update_box/1', data={"quantity": str(-sys.maxsize)}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(1).quantity != init_quan-sys.maxsize

def test_delete_box(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/delete_box/<int>' page is requested (POST)
    THEN: Check the box with the specified id is deleted
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    app = create_app()
    with app.app_context():
        if not Box.query.filter_by(name = "test2").all():
            name = "test2"
            quantity = 5
            size = "test"
            link = "test"
            image = "mule"
            # image.save("static/images/" + image.filename)
            low_stock = 0
            barcode = "test2"
            box = Box(name = name, quantity = quantity, size = size, link = link,
                    image = image, low_stock = low_stock, barcode = barcode)
            db.session.add(box)
            db.session.commit()

    #Does not work because database has been temporarily wiped
    with app.app_context():
        init_name = Box.query.get(1).name
    response = test_client.post('/delete_box/1', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(1) == None

def test_delete_admin_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/delete_admin/<int>' page is requested (POST)
    THEN: Check the admin with the specified id is deleted
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    app = create_app()
    with app.app_context():
        init_user = User.query.filter_by(email = "cyu25@colby.edu").first()
    
    print(init_user.id)

    response = test_client.post('/delete_admin/' + str(init_user.id), follow_redirects=True)
    #Should be taken to main.admin
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Delete Admin" in response.data

    with app.app_context():
        assert User.query.get(init_user.id) == None


def test_delete_yourself_failure(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/delete_admin/<int>' page is requested (POST)
    THEN: Check that you cannot delete yourself
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    app = create_app()
    with app.app_context():
        init_user = User.query.filter_by(email = "jhsmit25@colby.edu").first()

    response = test_client.post('/delete_admin/' + str(init_user.id), follow_redirects=True)
    #Should be taken to main.admin
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Delete Admin" in response.data

    #Verify Admin not deleted
    with app.app_context():
        assert User.query.get(init_user.id) == init_user




def test_add_box(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/add_box' page is requested (POST)
    THEN: Check the box is added to the database
    '''

    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    fake_file = (io.BytesIO(b"fake image content"), "test_image.png")

    conn = sqlite3.connect('instance/test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM box")
    # print("HERE", cursor.fetchone()[0])
    #Check if database is empty
    init_max = cursor.fetchone()[0]
    

    response = test_client.post('/add_box',
                data={
                'name': 'Test: ' + ''.join(random.choice(string.ascii_lowercase) for _ in range(12)),
                'quantity': 'test',
                'size': 'test',
                'link':  'test',
                'image':  fake_file,
                'low_stock':  5,
                'barcode': 'P' + ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
                },
            content_type='multipart/form-data',
            follow_redirects=True
        )

    print(response.data)
    #Should be redirected to main.admin
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Scan" in response.data

    conn = sqlite3.connect('instance/test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM box")
    #Verify database now has one additional box
    assert cursor.fetchone()[0] == init_max + 1


def test_add_user_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/add_user' page is requested (POST)
    THEN: Check the user is added to the database
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    conn = sqlite3.connect('instance/test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM user")
    init_max = cursor.fetchone()[0]



    response = test_client.post('/add_user',
                data={
                'email': ''.join(random.choice(string.ascii_lowercase) for _ in range(7)) + '@colby.edu',
                'password': ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
                },
            follow_redirects=True
        )

    print(response.data)
    #Should be redirected to main.admin
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Add New Admin" in response.data

    conn = sqlite3.connect('instance/test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM user")
    #Verify database now has one additional user
    assert cursor.fetchone()[0] == init_max + 1


def test_admin_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/admin' page is requested (POST)
    THEN: Check the user is taken to the admin page
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = test_client.get('/admin', follow_redirects=True)

    #Should be taken to admin page
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Admin" in response.data


def test_admin_failure(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/admin' page is requested (POST)
    THEN: Check the user is not allowed on admin page
    '''
    #Should not work because not logged in
    response = test_client.get('/admin', follow_redirects=True)

    #Should be taken to non-admin home page
    assert response.status_code == 200
    assert b"login" in response.data
    assert b"Admin" not in response.data
