from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class GoalForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[DataRequired(message="Informe o título da meta."), Length(max=120)],
    )
    description = TextAreaField(
        "Descrição",
        validators=[Optional(), Length(max=500)],
    )
    category = SelectField(
        "Categoria",
        choices=[
            ("casal", "Casal"),
            ("financas", "Finanças"),
            ("viagem", "Viagem"),
            ("casa", "Casa"),
            ("saude", "Saúde"),
            ("outros", "Outros"),
        ],
        default="casal",
    )
    priority = SelectField(
        "Prioridade",
        choices=[
            ("low", "Baixa"),
            ("medium", "Média"),
            ("high", "Alta"),
            ("critical", "Crítica"),
        ],
        default="medium",
    )
    status = SelectField(
        "Status",
        choices=[
            ("planned", "Planejada"),
            ("in_progress", "Em andamento"),
            ("paused", "Pausada"),
            ("completed", "Concluída"),
        ],
        default="planned",
    )
    progress = IntegerField(
        "Progresso",
        validators=[NumberRange(min=0, max=100)],
        default=0,
    )
    target_date = DateField("Data prevista", validators=[Optional()])
    favorite = BooleanField("Favorita")


class GoalFilterForm(FlaskForm):
    category = SelectField(
        "Categoria",
        choices=[
            ("", "Todas"),
            ("casal", "Casal"),
            ("financas", "Finanças"),
            ("viagem", "Viagem"),
            ("casa", "Casa"),
            ("saude", "Saúde"),
            ("outros", "Outros"),
        ],
        default="",
    )
    status = SelectField(
        "Status",
        choices=[
            ("", "Todos"),
            ("planned", "Planejada"),
            ("in_progress", "Em andamento"),
            ("paused", "Pausada"),
            ("completed", "Concluída"),
        ],
        default="",
    )
    sort_by = SelectField(
        "Ordenar por",
        choices=[("priority", "Prioridade"), ("target_date", "Data prevista")],
        default="priority",
    )
    order = SelectField(
        "Ordem",
        choices=[("desc", "Decrescente"), ("asc", "Crescente")],
        default="desc",
    )


class GoalProgressForm(FlaskForm):
    progress = IntegerField(
        "Progresso",
        validators=[
            DataRequired(message="Informe o progresso."),
            NumberRange(min=0, max=100),
        ],
    )
