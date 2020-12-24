from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# import os

'''
	TODO: Add passwords for users so that emails are not misused
		  Add course details section
		  Use CSS if possible
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IAmTheHeroOfAges'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sazed.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from coppermind import routes