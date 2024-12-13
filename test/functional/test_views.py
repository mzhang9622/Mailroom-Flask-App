import io
import sys
import sqlite3
import random
import string
from website import db
from website import create_app
from website.models import Box
from website.models import User

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
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    if not Box.query.filter_by(name = "test").all():
        response = test_client.post(
            '/add_box',
            data={
                'name': 'test',
                'quantity': '5',
                'size': 'test',
                'link': 'test',
                'image': (io.BytesIO(b'test image data'), 'test.png'),
                'low_stock': '0',
                'barcode': 'test',
            },
            content_type='multipart/form-data',  # Required for file uploads
            follow_redirects=True,
        )

    app = create_app()
    with app.app_context():
        init_quan = Box.query.filter_by(name = 'test').first().quantity
        id = Box.query.filter_by(name = 'test').first().id
    response = test_client.post('/update_box/' + str(id), json={'quantity': '5'}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.filter_by(name = 'test').first().quantity == init_quan+5


    #Check that system can handle overflow
    with app.app_context():
        init_quan = Box.query.get(id).quantity
    response = test_client.post('/update_box/' + str(id),
                                json={"quantity": str(sys.maxsize)}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(id).quantity != init_quan+sys.maxsize


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

    app = create_app()
    with app.app_context():
        init_quan = Box.query.filter_by(name = 'test').first().quantity
        id = Box.query.filter_by(name = 'test').first().id
    response = test_client.post('/update_box/' + str(id), json={"quantity": "-5"}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(id).quantity == init_quan-5


    #Check that system can handle overflow
    with app.app_context():
        init_quan = Box.query.filter_by(name = 'test').first().quantity
    response = test_client.post('/update_box/' + str(id),
                                json={"quantity": str(-sys.maxsize)}, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(id).quantity != init_quan-sys.maxsize

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
        if not Box.query.filter_by(name = "delete_test").all():
            name = "delete_test"
            quantity = 5
            size = "test"
            link = "test"
            image = "mule"
            # image.save("static/images/" + image.filename)
            low_stock = 0
            barcode = "delete_test"
            box = Box(id = 10000, name = name, quantity = quantity, size = size, link = link,
                    image = image, low_stock = low_stock, barcode = barcode)
            db.session.add(box)
            db.session.commit()

    #Does not work because database has been temporarily wiped
    # with app.app_context():
    #     init_name = Box.query.get(1).name
    response = test_client.post('/delete_box/10000', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.get(10000) is None

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

    response = test_client.post('/add_user',
                data={
                'email': "delete@colby.edu",
                'password': "delete"
                },
            follow_redirects=True
        )

    app = create_app()
    with app.app_context():
        init_user = User.query.filter_by(email = "delete@colby.edu").first()

    print(init_user.id)
    response = test_client.post('/delete_admin/' + str(init_user.id), follow_redirects=True)
    #Should be taken to main.admin
    assert response.status_code == 200
    assert b"logout" in response.data
    assert b"Delete Admin" in response.data

    with app.app_context():
        assert User.query.get(init_user.id) is None


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
                'name': 'Test: ' + ''.join(random.choice(string.ascii_lowercase)
                                           for _ in range(12)),
                'quantity': 10,
                'size': 'test',
                'link':  'test',
                'low_stock':  5,
                'barcode': 'P' + ''.join(random.choice(string.ascii_lowercase)
                                         for _ in range(12)),
                'image': fake_file
                },
            content_type='multipart/form-data',
            follow_redirects=True,
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

def test_login_get(test_client):
    '''
    Test Login
    '''
    # Simulate a POST request to /login with valid credentials    
    response = test_client.get('/login')

    assert response.status_code == 200
    print(response.data)
    assert b"login-input-container" in response.data

# def test_login_get_while_logged_in(test_client, valid_test_user):
#     # Simulate a POST request to /login with valid credentials
#     user = User() 
#     response = test_client.post(
#             '/login',
#             data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
#             follow_redirects=True
#         )

#     assert response.status_code == 200
#     print(response.data)
#     assert b"login-input-container" in response.data

def test_repeat_box_name(test_client):
    '''
        Test repeat box names
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = test_client.post(
            '/add_box',
            data={
                'name': 'test',
                'quantity': '5',
                'size': 'test',
                'link': 'test',
                'image': (io.BytesIO(b'test image data'), 'test.png'),
                'low_stock': '0',
                'barcode': 'test',
            },
            content_type='multipart/form-data',  # Required for file uploads
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b"ERROR: Box name already exists in database!" in response.data

def test_repeat_box_barcode(test_client):
    '''
    Test duplicate barcode
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = test_client.post(
            '/add_box',
            data={
                'name': 'new_test',
                'quantity': '5',
                'size': 'test',
                'link': 'test',
                'image': (io.BytesIO(b'test image data'), 'test.png'),
                'low_stock': '0',
                'barcode': 'test',
            },
            content_type='multipart/form-data',  # Required for file uploads
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b"ERROR: Barcode already exists in database!" in response.data

def test_negative_box_count(test_client):
    '''
        Test negative box count
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = test_client.post(
            '/add_box',
            data={
                'name': 'unique_name',
                'quantity': '-5',
                'size': 'test',
                'link': 'test',
                'image': (io.BytesIO(b'test image data'), 'test.png'),
                'low_stock': '0',
                'barcode': 'unique_barcode',
            },
            content_type='multipart/form-data',  # Required for file uploads
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b"ERROR: Box count cannot be negative!" in response.data

def test_negative_low_stock(test_client):
    '''
        Test negative low stock
    '''
    test_client.post(
            '/login',
            data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
            follow_redirects=True
        )

    response = test_client.post(
            '/add_box',
            data={
                'name': 'unique_name',
                'quantity': '5',
                'size': 'test',
                'link': 'test',
                'image': (io.BytesIO(b'test image data'), 'test.png'),
                'low_stock': '-5',
                'barcode': 'unique_barcode',
            },
            content_type='multipart/form-data',  # Required for file uploads
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b"ERROR: Low stock number cannot be negative!" in response.data


def test_update_non_existent_box(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is increased by the specified amount
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to add to non-existent box
    response = test_client.post('/update_box/19387', json={'quantity': '5'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

    #attempting to subtract from non-existent box
    response = test_client.post('/update_box/19387', json={'quantity': '-5'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

    #attempting to add 0 to non-existent box
    response = test_client.post('/update_box/19387', json={'quantity': '0'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data


def test_update_box_invalid_quantity(test_client):
    '''
    GIVEN: A Flask app configured for testing with a test test_client
    WHEN: The '/update_box/<int>' page is requested (POST)
    THEN: Check the box amount is increased by the specified amount
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    response = test_client.post('/update_box/2', json={'quantity': 'Hello'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid quantity value" in response.data

def test_update_size_success(test_client):
    '''
        Test update size
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    response = test_client.post('/update_size/2', json={'size': '10 x 10 x 10'}, follow_redirects=True)
    assert response.status_code == 200
    assert Box.query.get(2).size == '10 x 10 x 10'

def test_update_nonexistent_size(test_client):
    '''
        Test size
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with non-existent box
    response = test_client.post('/update_size/10938', json={'size': '10 x 10 x 10'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

def test_update_link_success(test_client):
    '''
        Test links
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    response = test_client.post('/update_link/2', json={'link': 'https://example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert Box.query.get(2).link == 'https://example.com'

def test_update_nonexistent_link(test_client):
    '''
        Test nonexistent links
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with non-existent box
    response = test_client.post('/update_link/10938', json={'link': 'https://example.com'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

def test_update_low_stock_success(test_client):
    '''
        Test low stock update
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    response = test_client.post('/update_low_stock/2', json={'low_stock': '0'}, follow_redirects=True)
    assert response.status_code == 200
    assert Box.query.get(2).low_stock == 0


def test_update_nonexistent_low_stock(test_client):
    '''
        Test invalid low stock
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with non-existent box
    response = test_client.post('/update_low_stock/10938', json={'low_stock': '0'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

def test_update_low_stock_success_2(test_client):
    '''
        Test low stock
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    response = test_client.post('/update_low_stock/2', json={'low_stock': 'hello'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid low stock value" in response.data

def test_update_barcode_success(test_client):
    '''
        Test barcode working
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with invalid quantity
    new_barcode = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
    response = test_client.post('/update_barcode/2', json={'barcode': new_barcode}, follow_redirects = True)
    assert response.status_code == 200
    assert Box.query.get(2).barcode == new_barcode

def test_update_repeat_barcode(test_client):
    '''
    Test update with repeat barcode
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with repeat barcode
    response = test_client.post('/update_barcode/2', json={'barcode': 'test'}, follow_redirects = True)
    assert response.status_code == 200
    assert b"Barcode must be unique" in response.data

def test_update_nonexistent_barcode(test_client):
    '''
        Test invalid barcode
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    #attempting to update with non-existent box
    new_barcode = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
    response = test_client.post('/update_barcode/10938', json={'barcode': new_barcode}, follow_redirects = True)
    assert response.status_code == 200
    assert b"Box not found" in response.data


def test_scan_box(test_client):
    '''
        Test scan
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    app = create_app()
    with app.app_context():
        id = Box.query.filter_by(name = 'test').first().id

    test_client.post('/update_box/' + str(id), json={'quantity': '1'}, follow_redirects=True)
    init_quan = Box.query.filter_by(name = 'test').first().quantity

    # test_client.post('/update_low_stock/' + str(id), json={'low_stock': '4'}, follow_redirects=True)
    response = test_client.post('/scan_box', data={'barcode': 'test'}, follow_redirects = True)
    assert response.status_code == 200
    with app.app_context():
        assert Box.query.filter_by(name = 'test').first().quantity == init_quan-1

def test_nonexistent_scan_box(test_client):
    '''
        Test scan for invalid box
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )


    response = test_client.post('/scan_box', data={'barcode': "nonexistent"}, follow_redirects = True)
    assert response.status_code == 200
    assert b"ERROR: Barcode does not exist in database!" in response.data

def test_nonexistent_delete_box(test_client):
    '''
        Test invalid delete box
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )
    response = test_client.post('/delete_box/982729', follow_redirects = True)
    assert response.status_code == 200
    assert b"Box not found" in response.data

def test_add_repeat_user(test_client):
    '''
        Test duplicate users
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )


    response = test_client.post('/add_user',
                                data = {'email': "jhsmit25@colby.edu",
                                        'password': "random"},
                                follow_redirects = True)
    assert response.status_code == 200
    assert b"ERROR: There is already an admin with that email!" in response.data

def test_add_invalid_user(test_client):
    '''
        Test invalid users
    '''
    test_client.post(
        '/login',
        data={'email': 'jhsmit25@colby.edu', 'password': 'jordan'},
        follow_redirects=True
    )

    response = test_client.post('/add_user',
                                data = {'email': "jhsmit25@bowdoin.edu",
                                        'password': "1234"},
                                follow_redirects = True)
    assert response.status_code == 200
    assert b"ERROR: Invalid email address! Please use a @colby.edu email." in response.data