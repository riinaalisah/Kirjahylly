import os
from os import urandom
from flask import Flask
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = urandom(32)

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# kirjautuminen


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Tämä toiminto vaatii kirjautumisen."
login_manager.login_message_category = 'info'

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'tsohakirjahylly@gmail.com'
app.config['MAIL_PASSWORD'] = 'nuxhatnhlegfdkfr'
mail = Mail(app)
mail.init_app(app)

from functools import wraps


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                if current_user.role == role:
                    unauthorized = False

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


# oman sovelluksen toiminnallisuudet
from application import views

from application.books import models
from application.books import views

from application.auth import models
from application.auth import views

from application.authors import models
from application.authors import views

# kirjautuminen osa 2

from application.auth.models import User
from application.auth.models import users_books


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# taulut tarvittaessa tietokantaan
try:
    db.create_all()
except:
    pass
