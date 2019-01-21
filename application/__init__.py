# flask-sovellus
from flask import Flask
app = Flask(__name__)

#tietokanta
from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
    app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

# oman sovelluksen toiminnallisuudet
from application import views

from application.books import models
from application.books import views

from application.auth import models
from application.auth import views

from application.authors import models
from application.authors import views

# kirjautuminen
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# taulut tarvittaessa tietokantaan
try:
    db.create_all()
except:
    pass
