from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import Length


class AuthorForm(FlaskForm):
    firstname = StringField("Kirjailijan etunimi", [Length(min=2, message="Kirjailijan etunimen tulee olla vähintään 2 merkkiä pitkä.")])
    lastname = StringField("Kirjailijan sukunimi", [validators.Length(min=2, message="Kirjailijan sukunimen tulee olla vähintään 2 merkkiä pitkä.")])

    class Meta:
        csrf = False
