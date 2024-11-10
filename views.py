from flask import Blueprint, render_template, request, redirect, url_for
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

    with open("box-inventory.csv", mode = "r", newline = "") as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            box = Box(name = row[0], quantity = 0, size = row[1], link = row[2], image = row[3])
            if not Box.query.filter_by(name = row[0]).all():
                db.session.add(box)
                db.session.commit()
            else:
                Box.query.filter_by(name = row[0]).first().update_attributes(size = row[1], link = row[2], image = row[3])
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

@main_blueprint.route('/update/<int:box_id>', methods=['GET', 'POST'])
@login_required
def update(box_id):
    if request.method == 'POST':
        box = Box.query.get(box_id)
        quantity = request.form['quantity']
        box.quantity = box.quantity + int(quantity)

        if box.quantity < 0:
            box.quantity = 0

        db.session.commit()

    return redirect(url_for('main.index'))