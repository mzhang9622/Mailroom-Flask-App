from flask import Flask
from models import db, User
from flask_login import LoginManager
from views import main_blueprint
from auth import auth_blueprint


website = Flask(__name__)

login_manager = LoginManager(website)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

website.register_blueprint(main_blueprint)
website.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    website.run(debug=True)
