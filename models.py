'''
models.py
'''

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    '''
    User: ids, emails, and passwords
    '''
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    def set_password(self, password):
        '''
        Set Password
        '''
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        '''
        Check Password
        '''
        return check_password_hash(self.password_hash, password)


class Box(db.Model):
    '''
    Box: ids, names, quantities, 
    sizes, links, images, low stocks,
    and barcode
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    quantity = db.Column(db.Integer, nullable = False)
    size = db.Column(db.String(200), nullable = False)
    link = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(200), nullable = False)
    low_stock = db.Column(db.Integer, nullable = False)
    barcode = db.Column(db.String(200), nullable = False, unique = True)
