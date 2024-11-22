'''
models.py
'''

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    '''
    User: ids and emails
    '''
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)

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
    barcode = db.Column(db.String(200), nullable = False)
