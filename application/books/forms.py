#Sisältää kirjojen käsittelyyn tarvittavat lomakkeet

from flask_wtf import FlaskForm
from wtforms import StringField

class BookForm(FlaskForm):
    name = StringField("Kirjan nimi")

    class Meta:
        csrf = False
