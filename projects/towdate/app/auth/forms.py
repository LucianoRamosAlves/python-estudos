from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# registro
class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])

    data_relacionamento = DateField(
        "Início do relacionamento",
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


# login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    remember = BooleanField("Lembrar-me")
