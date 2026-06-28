
from flask import Blueprint, render_template, url_for, redirect, flash

from app.models.user import User
from .forms import  RegisterForm, LoginForm
from app.extensions import db, bcrypt
from app.models.user import User
from flask_login import login_user, logout_user
from flask import session
import random

auth = Blueprint("auth", __name__)
cores = [
    {"fundo": "#DBEAFE", "icone": "#2563EB"},  # Azul
    {"fundo": "#DCFCE7", "icone": "#16A34A"},  # Verde
    {"fundo": "#FCE7F3", "icone": "#DB2777"},  # Rosa
    {"fundo": "#FEF3C7", "icone": "#D97706"},  # Dourado
    {"fundo": "#EDE9FE", "icone": "#7C3AED"},  # Roxo
    {"fundo": "#FFE4E6", "icone": "#E11D48"},  # Vermelho
]

cor = random.choice(cores)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            form.email.errors.append("E-mail não Cadastrado. Por favor Cadastre-se")
            flash("Falha no Login.", "error")

        elif user and not bcrypt.check_password_hash(user.password_hash, form.senha.data):
            form.senha.errors.append("Senha Inválida")
            flash("Falha no Login.", "error")

        elif user and bcrypt.check_password_hash(user.password_hash, form.senha.data):
            login_user(user, remember=form.remember.data)
            session["session_version"] = user.session_version
            flash("Seja Bem Vindo(a)", "success")
            return redirect(url_for("private.home"))

        # if form.is_submitted() and not form.validate():
        #     flash("Erro no login!", "error")

    return render_template("auth/login.html", form=form)



@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Aqui você pode adicionar a lógica para criar um novo usuário no banco de dados
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode("utf-8")
        cor = random.choice(cores)
        user = User(
            first_name=form.nome.data,
            last_name=form.sobrenome.data,
            email=form.email.data,
            date_of_birth=form.data_nascimento.data,
            password_hash=senha_hash,
            cor_fundo=cor["fundo"],
            cor_icone=cor["icone"],
            avatar="avatars/default.svg"
        )
        db.session.add(user) 
        db.session.commit()

        logout_user()      # Encerra qualquer sessão anterior
        login_user(user)


        flash(f"Registro bem-sucedido! {form.nome.data} {form.sobrenome.data}", "success")
        return redirect(url_for("private.home"))
  
    if form.is_submitted() and not form.validate():
        flash("Erro no registro!", "error")

    return render_template("auth/register.html", form=form)