from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.Length(min=2)])
    password = PasswordField("Salasana", [validators.Length(min=2)])

    class Meta:
        csrf = False


class UserForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2)])
    username = StringField("Käyttäjänimi", [validators.Length(min=2)])
    password = PasswordField("Salasana", [validators.Length(min=5)])

    class Meta:
        csrf = False


class EditForm(FlaskForm):
    name = StringField("Uusi nimi")
    username = StringField("Uusi käyttäjänimi")
    password = PasswordField("Uusi salasana")

    class Meta:
        csrf = False
