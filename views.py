from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, User, Box
import csv
from werkzeug.security import generate_password_hash

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    #this is very temporary
    if not User.query.filter_by(email = "cyu25@colby.edu").all():
        claire = User(email = "cyu25@colby.edu", password_hash = generate_password_hash("claire"))
        db.session.add(claire)
    if not User.query.filter_by(email = "jhsmit25@colby.edu").all():
        jordan = User(email = "jhsmit25@colby.edu", password_hash = generate_password_hash("jordan"))
        db.session.add(jordan)
    if not User.query.filter_by(email = "mzhang25@colby.edu").all():
        ming = User(email = "mzhang25@colby.edu", password_hash = generate_password_hash("ming"))
        db.session.add(ming)
    if not User.query.filter_by(email = "tjprat25@colby.edu").all():
        tim = User(email = "tjprat25@colby.edu", password_hash = generate_password_hash("tim"))
        db.session.add(tim)
    
    db.session.commit()

    if current_user.is_authenticated and current_user.email:
        return render_template('index.html', boxes = Box.query.all(), admin = True)

    return render_template('index.html', boxes = Box.query.all(), admin = False)

@main_blueprint.route("/about")
def about():
    if current_user.is_authenticated and current_user.email:
        return render_template('about.html', admin = True)
    
    return render_template('about.html', admin = False)

@main_blueprint.route("/contact")
def contact():
    if current_user.is_authenticated and current_user.email:
        return render_template('contact.html', admin = True)
    
    return render_template('contact.html', admin = False)

@main_blueprint.route('/login')
def login():
   if current_user.is_authenticated and current_user.email:
        return render_template('index.html', boxes = Box.query.all(), admin = True)
   
   return render_template('login.html')

@main_blueprint.route('/reset')
def reset():
   return render_template('reset.html')

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

        if box.quantity <= box.low_stock:
            flash(f'WARNING: Box {box.name} is low in stock!', 'warning')


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

@main_blueprint.route('/add_box', methods=['GET', 'POST'])
@login_required
def add_box():
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        link = request.form['link']
        image = request.files['image']
        image.save("static/images/" + image.filename)
        low_stock = request.form['low_stock']
        box = Box(name = name, quantity = 0, size = size, link = link, image = image.filename, low_stock = low_stock)
        db.session.add(box)
        db.session.commit()

    return redirect(url_for('main.index'))

@main_blueprint.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('All fields are required')
            return redirect(url_for('main.index'))
        
        if not email.endswith("@colby.edu"):
            flash('Invalid email')
            return redirect(url_for('main.index'))
        
        user = User(email = email, password_hash = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main.index'))