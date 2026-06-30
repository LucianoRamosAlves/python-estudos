from datetime import date
import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    DateField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.user import User


# registro
class RegisterForm(FlaskForm):

    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=50)])

    sobrenome = StringField(
        "Sobrenome", validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = EmailField("Email", validators=[DataRequired(), Email()])

    data_nascimento = DateField(
        "Data de Nascimento", validators=[DataRequired()], format="%Y-%m-%d"
    )

    termos = BooleanField(
        "Aceito os termos de uso",
        validators=[DataRequired(message="Você deve aceitar os termos de uso.")],
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            Length(
                min=8, max=128, message="A senha deve ter entre 8 e 128 caracteres."
            ),
        ],
    )
    confirmar_senha = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(),
            EqualTo("senha", message="As senhas devem ser iguais."),
        ],
    )

    def validate_nome(self, field):
        field.data = " ".join(field.data.split())

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
            raise ValidationError("O nome deve conter apenas letras.")

    def validate_sobrenome(self, field):
        field.data = " ".join(field.data.split())

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
            raise ValidationError("O sobrenome deve conter apenas letras.")

    def validate_email(self, email):
        email.data = email.data.strip().lower()

        user = User.query.filter_by(email=email.data).first()
        if user and user.id != getattr(current_user, "id", None):
            raise ValidationError("Este e-mail já cadastrado.")

    def validate_data_nascimento(self, field):
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


# login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar-me")

    def validate_email(self, email):
        email.data = email.data.strip().lower()  # Converte o email para minúsculas


# editar perfil
class EditProfileForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])

    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=50)])

    sobrenome = StringField(
        "Sobrenome", validators=[DataRequired(), Length(min=2, max=50)]
    )

    data_nascimento = DateField(
        "Data de Nascimento", validators=[DataRequired()], format="%Y-%m-%d"
    )

    def validate_nome(self, field):
        field.data = " ".join(field.data.split())

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
            raise ValidationError("O nome deve conter apenas letras.")

    def validate_sobrenome(self, field):
        field.data = " ".join(field.data.split())

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]+", field.data):
            raise ValidationError("O sobrenome deve conter apenas letras.")

    def validate_email(self, email):
        email.data = email.data.strip().lower()

        user = User.query.filter_by(email=email.data).first()
        if user and user.id != getattr(current_user, "id", None):
            raise ValidationError("Este e-mail já cadastrado.")

    def validate_data_nascimento(self, field):
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


class EditPhotoForm(FlaskForm):
    foto_perfil = FileField(
        "Foto de Perfil",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Apenas arquivos JPG, JPEG e PNG são permitidos.",
            )
        ],
    )


# mudar senha
class ChangePasswordForm(FlaskForm):
    senha_atual = PasswordField("Senha Atual", validators=[DataRequired()])
    nova_senha = PasswordField(
        "Nova Senha",
        validators=[
            DataRequired(),
            Length(
                min=8, max=128, message="A senha deve ter entre 8 e 128 caracteres."
            ),
        ],
    )
    confirmar_nova_senha = PasswordField(
        "Confirmar Nova Senha",
        validators=[
            DataRequired(),
            EqualTo("nova_senha", message="As senhas devem ser iguais."),
        ],
    )


# Encerrar sessões
class LogoutSessionsForm(FlaskForm):
    submit = SubmitField("Encerrar todas as sessões")


# Excluir conta
class DeleteAccountForm(FlaskForm):
    senha = PasswordField("Confirme sua senha", validators=[DataRequired()])

    submit = SubmitField("Excluir conta")
