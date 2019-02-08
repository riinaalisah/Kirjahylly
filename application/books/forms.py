from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length


class BookForm(FlaskForm):
    name = StringField("Kirjan nimi", validators=[Length(min=1, message="Pakollinen kenttä.")])

    class Meta:
        csrf = False
