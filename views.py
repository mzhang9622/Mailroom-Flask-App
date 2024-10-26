from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import User

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    return render_template('index.html')

@main_blueprint.route("/about")
def about(): 
    return render_template('about.html')

@main_blueprint.route("/contact")
def contact(): 
    return render_template('/contact.html')

@main_blueprint.route("/login")
def login(): 
    return render_template('login.html')

# @main_blueprint.route("/admin")
# @login_required
# def admin():
# check if admin, otherwise redirect to home redirect(url_for('index'))
# if 