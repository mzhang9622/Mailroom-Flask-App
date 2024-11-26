'''
__init__.py
'''

import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


db = SQLAlchemy()

def create_app(): 

    app = Flask(__name__)

    # check if testing, otherwise run per usual
    if os.environ.get('CONFIG_TYPE') == 'config.TestingConfig':
        app.config['SECRET_KEY'] = 'secret'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maildatabase.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    from .models import User
    from .views import main_blueprint
    from .auth import auth_blueprint
    

    @login_manager.user_loader
    def load_user(user_id):
        '''
        Get User
        '''
        return User.query.get(int(user_id))

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    create_app()