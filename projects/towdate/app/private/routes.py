# app/public/routes.py

from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required

from app.auth.forms import EditProfileForm
from app.extensions import db

private = Blueprint("private", __name__)


@private.route("/home")
@login_required
def home():
    return render_template("private/home/home.html")

@private.route("/sair")
@login_required
def sair():
    logout_user()
    return redirect(url_for("public.home"))

@private.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.first_name = form.nome.data
        current_user.last_name = form.sobrenome.data
        current_user.email = form.email.data
        current_user.date_of_birth = form.data_nascimento.data

        db.session.commit()

        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("private.account"))

    elif request.method == "GET":
        form.nome.data = current_user.first_name
        form.sobrenome.data = current_user.last_name
        form.email.data = current_user.email
        form.data_nascimento.data = current_user.date_of_birth

    return render_template(
        "private/accounts/account.html",
        active_page="account",
        form=form
    )

@private.route("/account/security")
@login_required
def account_security():
    return render_template(
        "private/accounts/security.html",
        active_page="security")

@private.route("/account/notifications")
@login_required
def account_notifications():
    return render_template(
        "private/accounts/notifications.html",
        active_page="notifications")

@private.route("/account/preferences")
@login_required
def account_preferences():
    return render_template(
        "private/accounts/preferences.html",
        active_page="preferences")