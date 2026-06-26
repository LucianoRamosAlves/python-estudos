
from flask import Blueprint, render_template, url_for, redirect, flash
from .forms import  RegisterForm, LoginForm
from app.extensions import db, bcrypt
from app.models.user import User
from flask_login import login_user

auth = Blueprint("auth", __name__)

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
        user = User(
            first_name=form.nome.data,
            last_name=form.sobrenome.data,
            email=form.email.data,
            birth_date=form.data_nascimento.data,
            password_hash=senha_hash
        )
        db.session.add(user) 
        db.session.commit()
        flash(f"Registro bem-sucedido! {form.nome.data} {form.sobrenome.data}", "success")
        return redirect(url_for("private.home"))
  
    if form.is_submitted() and not form.validate():
        flash("Erro no registro!", "error")

    return render_template("auth/register.html", form=form)