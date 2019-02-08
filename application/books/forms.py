from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length


class BookForm(FlaskForm):
    name = StringField("Kirjan nimi", validators=[Length(min=1, message="Pakollinen kenttä.")])
    pages = IntegerField("Sivuja")
    isbn = StringField("ISBN-koodi")

    class Meta:
        csrf = False
