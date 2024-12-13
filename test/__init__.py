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
