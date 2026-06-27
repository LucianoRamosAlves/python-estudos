from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, PasswordField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User
from flask_login import current_user
from flask import flash


# registro
class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])

    data_nascimento = DateField(
        "Data de Nascimento",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )

    termos = BooleanField("Aceito os termos de uso", validators=[DataRequired(message="Você deve aceitar os termos de uso.")])

    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    confirmar_senha = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(),
            EqualTo("senha", message="As senhas devem ser iguais.")
        ]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro e-mail ou faça o login para continuar ')


# login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    remember = BooleanField("Lembrar-me")

#editar perfil
class EditProfileForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
  
    data_nascimento = DateField(
        "Data de Nascimento",
        validators=[DataRequired()],
        format="%Y-%m-%d"
    )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Erro ao atualizar dados.', 'error')
                raise ValidationError('Email já cadastrado. Cadastre-se com outro e-mail ou mantenha o e-mail atual.')


class EditPhotoForm(FlaskForm):
    foto_perfil = FileField(
        "Foto de Perfil",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Apenas arquivos JPG, JPEG e PNG são permitidos."
            )
        ]
    )

#mudar senha
class ChangePasswordForm(FlaskForm):
    senha_atual = PasswordField("Senha Atual", validators=[DataRequired()])
    nova_senha = PasswordField("Nova Senha", validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    confirmar_nova_senha = PasswordField(
        "Confirmar Nova Senha",
        validators=[
            DataRequired(),
            EqualTo("nova_senha", message="As senhas devem ser iguais.")
        ]
    )

# Encerrar sessões
class LogoutSessionsForm(FlaskForm):
    submit = SubmitField("Encerrar todas as sessões")

# # Excluir conta
# class DeleteAccountForm(FlaskForm):
#     submit = SubmitField("Excluir conta")
