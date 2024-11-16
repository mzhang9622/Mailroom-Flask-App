from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from models import User
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user

# Create a blueprint
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))