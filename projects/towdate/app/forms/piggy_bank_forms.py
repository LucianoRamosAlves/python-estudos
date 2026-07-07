from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class PiggyBankForm(FlaskForm):
    """Formulário para criar ou editar um cofrinho."""

    title = StringField(
        "Título",
        validators=[
            DataRequired(message="Informe o título do cofrinho."),
            Length(max=120),
        ],
    )
    description = TextAreaField(
        "Descrição",
        validators=[Optional(), Length(max=500)],
    )
    target_amount = FloatField(
        "Valor da meta",
        validators=[
            DataRequired(message="Informe o valor da meta."),
            NumberRange(min=0.01),
        ],
    )
    current_amount = FloatField(
        "Valor atual",
        validators=[
            DataRequired(message="Informe o valor atual."),
            NumberRange(min=0.0),
        ],
    )
    category = SelectField(
        "Categoria",
        choices=[
            ("casal", "Casal"),
            ("viagem", "Viagem"),
            ("casa", "Casa"),
            ("presente", "Presente"),
            ("outros", "Outros"),
        ],
        default="casal",
    )
    target_date = DateField("Data prevista", validators=[Optional()])
    status = SelectField(
        "Status",
        choices=[
            ("planned", "Planejado"),
            ("in_progress", "Em andamento"),
            ("completed", "Concluído"),
        ],
        default="planned",
    )
    favorite = BooleanField("Favorito")


class PiggyBankMovementForm(FlaskForm):
    """Formulário para registrar uma movimentação."""

    amount = FloatField(
        "Valor",
        validators=[
            DataRequired(message="Informe o valor do depósito."),
            NumberRange(min=0.01),
        ],
    )
    observation = TextAreaField("Observação", validators=[Optional(), Length(max=500)])
