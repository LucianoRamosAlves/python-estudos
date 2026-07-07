from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    HiddenField,
    IntegerField,
    MultipleFileField,
    StringField,
    TextAreaField,
)
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class MemoryCreateForm(FlaskForm):
    """Formulario para cadastrar uma nova memoria."""

    photos = MultipleFileField("Fotos")

    title = StringField(
        "Titulo",
        validators=[
            DataRequired(message="O titulo da memoria e obrigatorio."),
            Length(max=120, message="O titulo deve ter no maximo 120 caracteres."),
        ],
    )

    description = TextAreaField(
        "Descricao",
        validators=[
            DataRequired(message="A descricao da memoria e obrigatoria."),
            Length(max=280, message="A descricao pode ter no maximo 280 caracteres."),
        ],
    )

    memory_date = DateField(
        "Data",
        format="%Y-%m-%d",
        validators=[DataRequired(message="A data da memoria e obrigatoria.")],
    )

    location = StringField(
        "Localizacao",
        validators=[
            Optional(),
            Length(max=120, message="A localizacao deve ter no maximo 120 caracteres."),
        ],
    )

    collection_slug = HiddenField(
        "Colecao",
        validators=[DataRequired(message="Escolha uma colecao para a memoria.")],
    )

    custom_collection_name = HiddenField(
        "Nova colecao",
        validators=[Optional(), Length(max=80)],
    )

    tags = HiddenField("Tags", validators=[Optional()])

    rating = IntegerField(
        "Avaliacao",
        validators=[
            DataRequired(message="A avaliacao da memoria e obrigatoria."),
            NumberRange(min=1, max=5, message="A avaliacao deve ser entre 1 e 5."),
        ],
    )

    favorite = BooleanField("Favorita")

    def validate_memory_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError("A data da memoria nao pode estar no futuro.")

    def validate_photos(self, field):
        photos = [
            photo for photo in (field.data or []) if getattr(photo, "filename", "")
        ]
        if not photos:
            raise ValidationError(
                "Adicione pelo menos uma foto para registrar a memoria."
            )


class MemoryUpdateForm(FlaskForm):
    """Formulario para editar uma memoria existente."""

    title = StringField(
        "Titulo",
        validators=[
            DataRequired(message="O titulo da memoria e obrigatorio."),
            Length(max=120, message="O titulo deve ter no maximo 120 caracteres."),
        ],
    )

    description = TextAreaField(
        "Descricao",
        validators=[
            DataRequired(message="A descricao da memoria e obrigatoria."),
            Length(max=280, message="A descricao pode ter no maximo 280 caracteres."),
        ],
    )

    memory_date = DateField(
        "Data",
        format="%Y-%m-%d",
        validators=[DataRequired(message="A data da memoria e obrigatoria.")],
    )

    location = StringField(
        "Localizacao",
        validators=[
            Optional(),
            Length(max=120, message="A localizacao deve ter no maximo 120 caracteres."),
        ],
    )

    collection_slug = StringField(
        "Colecao",
        validators=[
            DataRequired(message="Escolha uma colecao para a memoria."),
            Length(max=80),
        ],
    )

    custom_collection_name = StringField(
        "Nova colecao",
        validators=[Optional(), Length(max=80)],
    )

    tags = StringField("Tags", validators=[Optional(), Length(max=255)])

    rating = IntegerField(
        "Avaliacao",
        validators=[
            DataRequired(message="A avaliacao da memoria e obrigatoria."),
            NumberRange(min=1, max=5, message="A avaliacao deve ser entre 1 e 5."),
        ],
    )

    favorite = BooleanField("Favorita")

    def validate_memory_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError("A data da memoria nao pode estar no futuro.")


class MemoryDeleteForm(FlaskForm):
    """Formulario simples para remover memoria com CSRF."""

    pass
