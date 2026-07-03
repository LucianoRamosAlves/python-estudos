# REPETICÇAO DE CÓDIGO
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    DateField,
    BooleanField,
    SubmitField,
)
from app.auth.validators import (
    validar_nome,
    validar_sobrenome,
    validar_email,
    validar_data_nascimento,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
 
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
        validar_nome(field)

    def validate_sobrenome(self, field):
        validar_sobrenome(field)

    def validate_email(self, field):
        validar_email(field)

    def validate_data_nascimento(self, field):
        validar_data_nascimento(field)

# login
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    remember = BooleanField("Lembrar-me")

    def validate_email(self, field):
        field.data = field.data.strip().lower()


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
        validar_nome(field)

    def validate_sobrenome(self, field):
        validar_sobrenome(field)

    def validate_email(self, field):
        validar_email(field)

    def validate_data_nascimento(self, field):
        validar_data_nascimento(field)


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
