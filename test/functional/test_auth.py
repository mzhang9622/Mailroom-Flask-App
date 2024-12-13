from app import create_app
from website.models import Box
from website.models import User
from website import db
from werkzeug.security import generate_password_hash

def test_login_success(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/login' page is requested (POST)
    THEN: Check the user is taken to the main admin page
    '''
    app = create_app()
    with app.app_context():
        if not User.query.filter_by(email = "jhsmit25@colby.edu").all():
            user = User(email = "jhsmit25@colby.edu",
                        password_hash = generate_password_hash('jordan'))
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