from flask import Blueprint, render_template
from flask_login import current_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def index():
    if current_user.is_authenticated and current_user.username:
        return render_template('admin.html')
    return render_template('index.html')

@main_blueprint.route("/about")
def about(): 
    return render_template('about.html')

@main_blueprint.route("/contact")
def contact(): 
    return render_template('contact.html')