#Sisältää kirjojen käsittelyyn tarvittavat lomakkeet

from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import InputRequired


class BookForm(FlaskForm):
    author_firstname = StringField("Kirjailijan etunimi", [validators.Length(min=2)])
    author_lastname = StringField("Kirjailijan sukunimi", [validators.Length(min=2)])
    name = StringField("Kirjan nimi", [InputRequired()])

    class Meta:
        csrf = False
