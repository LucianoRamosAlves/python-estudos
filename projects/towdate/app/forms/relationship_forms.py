from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField
from wtforms import DateField
from flask_wtf.file import FileField, FileAllowed

class RelationshipForm(FlaskForm):

    relationship_status = SelectField(
    "Status",
    choices=[
        ("namorando", "💖 Namorando"),
        ("casados", "💍 Casados"),
        ("noivos", "💖 Noivos"),
        ("uniao_estavel", "❤️ União estável"),
    ],
    validators=[DataRequired()],
)

    relationship_phrase = TextAreaField(
    "Frase do casal",
    validators=[
        Length(max=255)
    ]
)

    relationship_start_date = DateField(
    "Data de início",
    format="%Y-%m-%d",
    validators=[DataRequired()]
)

    couple_photo = FileField(
    "Foto do casal",
    validators=[
        FileAllowed(
            ["jpg", "jpeg", "png", "webp"],
            "Apenas imagens JPG, JPEG, PNG e WEBP são permitidas."
        )
    ]
)