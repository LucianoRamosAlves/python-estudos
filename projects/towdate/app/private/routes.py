# app/public/routes.py

from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required

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

@private.route("/account")
@login_required
def account():
    return render_template(
        "private/accounts/account.html",
        active_page="account")

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