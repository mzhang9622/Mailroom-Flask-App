'''
models.py: organization for the database
'''

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

'''
User: ids and emails
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)

'''
Box: ids, names, quantities, 
sizes, links, images, low stocks,
and barcode
'''
class Box(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False, unique = True)
    quantity = db.Column(db.Integer, nullable = False)
    size = db.Column(db.String(200), nullable = False)
    link = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(200), nullable = False)
    low_stock = db.Column(db.Integer, nullable = False)
    barcode = db.Column(db.String(200), nullable = False)
