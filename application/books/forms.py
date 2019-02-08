from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


class BookForm(FlaskForm):
    name = StringField("Kirjan nimi", validators=[InputRequired()])

    class Meta:
        csrf = False
