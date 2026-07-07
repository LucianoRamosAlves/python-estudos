from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional, URL, NumberRange


class WishForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[
            DataRequired(message="Informe o título do desejo."),
            Length(max=120),
        ],
    )
    description = TextAreaField("Descrição", validators=[Optional(), Length(max=500)])
    category = SelectField(
        "Categoria",
        choices=[
            ("viagem", "Viagem"),
            ("restaurante", "Restaurante"),
            ("cinema", "Cinema"),
            ("serie", "Série"),
            ("livro", "Livro"),
            ("presente", "Presente"),
            ("experiencia", "Experiência"),
            ("casa", "Casa"),
            ("compras", "Compras"),
            ("outro", "Outro"),
        ],
        default="outro",
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
        choices=[("pending", "Pendente"), ("completed", "Realizado")],
        default="pending",
    )
    favorite = BooleanField("Favorito")
    link = StringField(
        "Link", validators=[Optional(), URL(message="Informe um link válido.")]
    )
    price_estimated = DecimalField(
        "Preço estimado", validators=[Optional(), NumberRange(min=0)], places=2
    )
    planned_date = DateField("Data prevista", validators=[Optional()])


class WishFilterForm(FlaskForm):
    category = SelectField(
        "Categoria",
        choices=[
            ("", "Todas"),
            ("viagem", "Viagem"),
            ("restaurante", "Restaurante"),
            ("cinema", "Cinema"),
            ("serie", "Série"),
            ("livro", "Livro"),
            ("presente", "Presente"),
            ("experiencia", "Experiência"),
            ("casa", "Casa"),
            ("compras", "Compras"),
            ("outro", "Outro"),
        ],
        default="",
    )
    status = SelectField(
        "Status",
        choices=[("", "Todos"), ("pending", "Pendente"), ("completed", "Realizado")],
        default="",
    )
    sort_by = SelectField(
        "Ordenar por",
        choices=[("created_at", "Data de criação"), ("planned_date", "Data prevista")],
        default="created_at",
    )
    order = SelectField(
        "Ordem",
        choices=[("desc", "Decrescente"), ("asc", "Crescente")],
        default="desc",
    )
