from flask_wtf import FlaskForm
from wtforms import StringField, validators

class AuthorForm(FlaskForm):
    firstname = StringField("Kirjailijan etunimi", [validators.Length(min=2)])
    lastname = StringField("Kirjailijan sukunimi", [validators.Length(min=2)])

    class Meta:
        csrf = False
