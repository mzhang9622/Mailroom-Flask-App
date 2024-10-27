from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Box(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    quantity = db.Column(db.Integer, nullable = False)
    size = db.Column(db.String(200), nullable = False)
    link = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(200), nullable = False)

    def update_attributes(self, size, link, image):
        self.size = size
        self.link = link
        self.image = image
