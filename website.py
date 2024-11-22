'''
website.py
'''

import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask import Flask
from models import db
from models import User
from views import main_blueprint
from auth import auth_blueprint

load_dotenv()

website = Flask(__name__)
website.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maildatabase.db'
website.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(website)
login_manager = LoginManager(website)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    '''
    Get User
    '''
    return User.query.get(int(user_id))

website.register_blueprint(main_blueprint)
website.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    with website.app_context():
        db.create_all()
    website.run(debug=True)
