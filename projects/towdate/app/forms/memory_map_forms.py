from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, SelectField, StringField
from wtforms.validators import Optional, Length


class MemoryMapFilterForm(FlaskForm):
    category = SelectField("Categoria", choices=[], default="")
    date_from = DateField("De", validators=[Optional()])
    date_to = DateField("Até", validators=[Optional()])
    city = StringField("Cidade", validators=[Optional(), Length(max=80)])
    favorites_only = BooleanField("Apenas favoritos")
