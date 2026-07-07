from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class CalendarEventForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[
            DataRequired(message="Informe o título do evento."),
            Length(max=120),
        ],
    )
    description = TextAreaField(
        "Descrição",
        validators=[Optional(), Length(max=500)],
    )
    event_date = DateField(
        "Data",
        validators=[DataRequired(message="Informe a data do evento.")],
    )
    event_time = StringField("Horário", validators=[Optional(), Length(max=10)])
    location = StringField("Local", validators=[Optional(), Length(max=120)])
    category = SelectField(
        "Categoria",
        choices=[
            ("personal", "Pessoal"),
            ("date", "Data"),
            ("trip", "Viagem"),
            ("special", "Especial"),
        ],
        default="personal",
    )
    favorite = BooleanField("Favorito")
