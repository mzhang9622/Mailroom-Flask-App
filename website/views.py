'''
views.py
'''

import os
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import flash
from flask import jsonify
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import generate_password_hash
from website import db
from .models import User
from .models import Box
from .util import send_email

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    '''
    Main page
    '''
    #this is very temporary
    if not User.query.filter_by(email = "darmstro@colby.edu").all():
        deanna = User(email = "darmstro@colby.edu",
                      password_hash = generate_password_hash(os.environ.get('MAILROOM_PASSWORD')))
        db.session.add(deanna)

    db.session.commit()

    if current_user.is_authenticated and current_user.email:
        return render_template('index.html', boxes = Box.query.all(),
            users = User.query.all(), admin = True)

    return render_template('index.html', boxes = Box.query.all(),
        users = User.query.all(), admin = False)

@main_blueprint.route("/about")
def about():
    '''
    About page
    '''
    if current_user.is_authenticated and current_user.email:
        return render_template('about.html', admin = True)
    return render_template('about.html', admin = False)


@main_blueprint.route("/contact")
def contact():
    '''
    Contact Page
    '''
    access_key = os.getenv("WEB3FORMS_ACCESS_KEY")
    if current_user.is_authenticated and current_user.email:
        return render_template('contact.html', admin = True, access_key=access_key)

    return render_template('contact.html', admin = False, access_key=access_key)

@main_blueprint.route("/login", methods=['GET'])
def login():
    '''
    Login Page
    '''
    if current_user.is_authenticated and current_user.email:
        return render_template('index.html', boxes = Box.query.all(),
            users = User.query.all(), admin = True)

    return render_template('login.html')

@main_blueprint.route('/admin', methods =['GET'])
@login_required
def admin():
    '''
    Admin Page
    '''
    if current_user.is_authenticated and current_user.email:
        return render_template('admin.html',  users = User.query.all(), admin = True)
    return render_template('index.html', boxes = Box.query.all(),
        users = User.query.all(), admin = False)

@main_blueprint.route('/add_box', methods=['GET', 'POST'])
@login_required
def add_box():
    '''
    Add Boxes
    '''
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        size = request.form['size']
        link = request.form['link']
        image = request.files['image']
        image.save("website/static/images/" + image.filename)
        low_stock = request.form['low_stock']
        barcode = request.form['barcode']

        if Box.query.filter_by(name = name).first():
            flash('ERROR: Box name already exists in database!', 'error')
            return redirect(url_for('main.index'))
        if Box.query.filter_by(barcode = barcode).first():
            flash('ERROR: Barcode already exists in database!', 'error')
            return redirect(url_for('main.index'))
        if int(quantity) < 0:
            flash('ERROR: Box count cannot be negative!', 'error')
            return redirect(url_for('main.index'))
        if int(low_stock) < 0:
            flash('ERROR: Low stock number cannot be negative!', 'error')
            return redirect(url_for('main.index'))

        box = Box(name = name, quantity = quantity, size = size, link = link,
                image = image.filename, low_stock = low_stock, barcode = barcode)
        db.session.add(box)
        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/update_box/<int:box_id>', methods=['POST'])
@login_required
def update_box(box_id):
    '''
    Update Count
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    quantity = request.json.get('quantity', 0)

    try:
        quantity = int(quantity)
        if quantity > 1000:
            return jsonify({'success': False, 'message': 'Amount entered is too high!'})

        box.quantity += quantity
        box.quantity = max(box.quantity, 0)

        if box.quantity <= box.low_stock:
            email_content = f"""
                <p>Dear Admin,</p>
                <p>The stock for <strong>{box.name}</strong> is running low.</p>
                <ul>
                    <li>Current Quantity: {box.quantity}</li>
                    <li>Low Stock Threshold: {box.low_stock}</li>
                </ul>
                <p>Please restock soon.</p>
            """
            send_email(
                subject=f"Low Stock Alert: {box.name}",
                to_email='darmstro@colby.edu',
                html_content=email_content
            )

        db.session.commit()

        return jsonify({'success': True, 'new_quantity': box.quantity})
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity value'})

@main_blueprint.route('/update_size/<int:box_id>', methods=['POST'])
@login_required
def update_size(box_id):
    '''
    Update Size
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    size = request.json.get('size', 0)

    box.size = size
    db.session.commit()

    return jsonify({'success': True, 'new_size': box.size})

@main_blueprint.route('/update_link/<int:box_id>', methods=['POST'])
@login_required
def update_link(box_id):
    '''
    Update Link
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    link = request.json.get('link', 0)

    box.link = link
    db.session.commit()

    return jsonify({'success': True, 'new_link': box.link})

@main_blueprint.route('/update_low_stock/<int:box_id>', methods=['POST'])
@login_required
def update_low_stock(box_id):
    '''
    Update Low Stock Number
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    low_stock = request.json.get('low_stock', 0)
    try:
        low_stock = int(low_stock)
        box.low_stock = low_stock
        box.low_stock = max(box.low_stock, 0)
        db.session.commit()

        return jsonify({'success': True, 'new_low_stock': box.low_stock})
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid low stock value'})

@main_blueprint.route('/update_barcode/<int:box_id>', methods=['POST'])
@login_required
def update_barcode(box_id):
    '''
    Update Barcode
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    barcode = request.json.get('barcode', 0)
    if Box.query.filter_by(barcode = barcode).first():
        return jsonify({'success': False, 'message': 'Barcode must be unique!'})

    box.barcode = barcode
    db.session.commit()

    return jsonify({'success': True, 'new_barcode': box.barcode})

@main_blueprint.route('/scan_box', methods=['GET', 'POST'])
@login_required
def scan_box():
    '''
    Scan Boxes
    '''
    if request.method == 'POST':
        barcode = request.form['barcode']

        if not Box.query.filter_by(barcode = barcode).first():
            flash('ERROR: Barcode does not exist in database!', 'error')
            return redirect(url_for('main.index'))
        box = Box.query.filter_by(barcode = barcode).first()
        box.quantity -= 1
        box.quantity = max(box.quantity, 0)

        if box.quantity <= box.low_stock:
            email_content = f"""
                <p>Dear Admin,</p>
                <p>The stock for <strong>{box.name}</strong> is running low.</p>
                <ul>
                    <li>Current Quantity: {box.quantity}</li>
                    <li>Low Stock Threshold: {box.low_stock}</li>
                </ul>
                <p>Please restock soon.</p>
            """
            send_email(
                subject=f"Low Stock Alert: {box.name}",
                to_email='darmstro@colby.edu',
                html_content=email_content
            )

        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_box/<int:box_id>', methods=['POST'])
@login_required
def delete_box(box_id):
    '''
    Delete Boxes
    '''
    box = Box.query.get(box_id)
    if not box:
        return jsonify({'success': False, 'message': 'Box not found'})

    db.session.delete(box)
    db.session.commit()

    return jsonify({'success': True})

@main_blueprint.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    '''
    Add Users
    '''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email = email).first():
            flash('ERROR: There is already an admin with that email!', 'error')
            return redirect(url_for('main.admin'))

        if not email.endswith("@colby.edu"):
            flash('ERROR: Invalid email address! Please use a @colby.edu email.', 'error')
            return redirect(url_for('main.admin'))

        user = User(email = email, password_hash = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main.admin'))

@main_blueprint.route('/delete_admin/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_admin(user_id):
    '''
    Delete Admins
    '''
    if request.method == 'POST':
        user = User.query.get(user_id)
        if (user.email != current_user.email) and (db.session.query(User).count() != 1):
            print(current_user)
            db.session.delete(user)
            db.session.commit()

    return redirect(url_for('main.admin'))
