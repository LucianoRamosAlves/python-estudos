import re

from datetime import date

from flask_login import current_user
from wtforms.validators import ValidationError

from app.models.user import User


def validar_nome(field):
    field.data = " ".join(field.data.split())

    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
        raise ValidationError("O nome deve conter apenas letras.")

def validar_sobrenome(field):
    field.data = " ".join(field.data.split())

    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
        raise ValidationError("O sobrenome deve conter apenas letras.")

def validar_email(field):
    field.data = field.data.strip().lower()

    user = User.query.filter_by(email=field.data).first()
    if user and user.id != getattr(current_user, "id", None):
        raise ValidationError("Este e-mail já cadastrado.")

def validar_data_nascimento(field):
    hoje = date.today()

    # Não permite datas futuras
    if field.data > hoje:
        raise ValidationError("A data de nascimento não pode ser futura.")

    # Idade mínima (exemplo: 18 anos)
    idade = hoje.year - field.data.year
    if (hoje.month, hoje.day) < (field.data.month, field.data.day):
        idade -= 1

    if idade < 18:
        raise ValidationError("É necessário ter pelo menos 18 anos.")