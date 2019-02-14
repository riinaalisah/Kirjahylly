from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False


class UserForm(FlaskForm):
    name = StringField("Nimi", [Length(min=2, message="Nimen tulee olla vähintään 2 merkkiä pitkä.")])
    username = StringField("Käyttäjänimi",
                           [Length(min=2, message="Käyttäjänimen tulee olla vähintään 2 merkkiä pitkä.")])
    password = PasswordField("Salasana", [Length(min=5, message="Salasanan tulee olla vähintään 5 merkkiä pitkä.")])

    class Meta:
        csrf = False


class EditForm(FlaskForm):
    name = StringField("Uusi nimi")
    username = StringField("Uusi käyttäjänimi")
    password = PasswordField("Uusi salasana")

    class Meta:
        csrf = False


