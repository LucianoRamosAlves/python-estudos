from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class PartnerConnectForm(FlaskForm):
    partner_code = StringField(
        "Digite o código",
        validators=[
            DataRequired(message="Informe um código de convite válido."),
            Length(max=255),
        ],
    )


class PartnerDisconnectForm(FlaskForm):
    pass
