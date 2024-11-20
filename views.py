from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import current_user
from flask_login import login_required
from models import db
from models import User
from models import Box
import os

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    #this is very temporary
    if not User.query.filter_by(email = "cyu25@colby.edu").all():
        claire = User(email = "cyu25@colby.edu")
        db.session.add(claire)
    if not User.query.filter_by(email = "jhsmit25@colby.edu").all():
        jordan = User(email = "jhsmit25@colby.edu")
        db.session.add(jordan)
    if not User.query.filter_by(email = "mzhang25@colby.edu").all():
        ming = User(email = "mzhang25@colby.edu")
        db.session.add(ming)
    if not User.query.filter_by(email = "tjprat25@colby.edu").all():
        tim = User(email = "tjprat25@colby.edu")
        db.session.add(tim)
    
    db.session.commit()

    if current_user.is_authenticated and current_user.email:
        return render_template('index.html', boxes = Box.query.all(), users = User.query.all(), admin = True)

    return render_template('index.html', boxes = Box.query.all(), users = User.query.all(), admin = False)

@main_blueprint.route("/about")
def about():
    if current_user.is_authenticated and current_user.email:
        return render_template('about.html', admin = True)
    
    return render_template('about.html', admin = False)

@main_blueprint.route("/contact")
def contact():
    access_key = os.getenv("WEB3FORMS_ACCESS_KEY")
    if current_user.is_authenticated and current_user.email:
        return render_template('contact.html', admin = True, access_key=access_key)
    
    return render_template('contact.html', admin = False, access_key=access_key)

@main_blueprint.route('/update_box/<int:box_id>', methods=['GET', 'POST'])
@login_required
def update_box(box_id):
    if request.method == 'POST':
        box = Box.query.get(box_id)
        quantity = request.form['quantity']

        if quantity == '':
            quantity = 0

        box.quantity = box.quantity + int(quantity)

        if box.quantity < 0:
            box.quantity = 0
        
        boxes = Box.query.all()
        for box in boxes: 
            if box.quantity <= box.low_stock:
                flash(f'WARNING: {box.name} is low in stock!', 'warning')


        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_box/<int:box_id>', methods=['GET', 'POST'])
@login_required
def delete_box(box_id):
    if request.method == 'POST':
        box = Box.query.get(box_id)
        db.session.delete(box)
        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_admin/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_admin(user_id):
    if request.method == 'POST':
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('main.admin'))

@main_blueprint.route('/add_box', methods=['GET', 'POST'])
@login_required
def add_box():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        size = request.form['size']
        link = request.form['link']
        image = request.files['image']
        image.save("static/images/" + image.filename)
        low_stock = request.form['low_stock']
        barcode = request.form['barcode']
        box = Box(name = name, quantity = quantity, size = size, link = link, image = image.filename, low_stock = low_stock, barcode = barcode)
        db.session.add(box)
        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        
        if not email.endswith("@colby.edu"):
            flash('ERROR: Invalid email address! Please use a @colby.edu email.', 'error')
            return redirect(url_for('main.admin'))
        
        user = User(email = email)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main.admin'))

@main_blueprint.route('/admin')
def admin():
    if current_user.is_authenticated and current_user.email:
        return render_template('admin.html',  users = User.query.all(), admin = True)