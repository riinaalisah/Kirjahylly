from flask_wtf import FlaskForm
from wtforms import StringField, validators

class AuthorForm(FlaskForm):
    firstname = StringField("Etunimi", [validators.Length(min=2)])
    lastname = StringField("Sukunimi", [validators.Length(min=2)])

    class Meta:
        csrf = False
