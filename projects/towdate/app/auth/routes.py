
from flask import Blueprint, render_template, url_for, redirect, flash
from .forms import  RegisterForm, LoginForm
from app.extensions import db, bcrypt
from app.models.user import User
from flask_login import login_user, logout_user
from flask import session
from app.services.avatar_colors import cores
import random

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, form.senha.data):
            form.email.errors.append("Verifique o E-mail.")
            form.senha.errors.append("Verifique a senha.")
            flash("Falha no Login.", "error")

        else:
            login_user(user, remember=form.remember.data)
            session["session_version"] = user.session_version

            flash("Seja Bem Vindo(a)", "success")
            return redirect(url_for("private.home"))


    return render_template("auth/login.html", form=form)



@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
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
            avatar=None
        )
        
        db.session.add(user) 
        db.session.commit()

        login_user(user)
        session["session_version"] = user.session_version


        flash(f"Registro bem-sucedido! {user.full_name}", "success")
        return redirect(url_for("private.home"))
  
    if form.is_submitted() and not form.validate():
        flash("Erro no registro!", "error")

    return render_template("auth/register.html", form=form)