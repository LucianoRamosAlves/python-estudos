
from flask import Blueprint, render_template, url_for, redirect, flash

from .forms import  RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f"Login bem-sucedido! {form.email.data}", "success")
        return redirect(url_for("private.home"))

    else:
        flash("Erro no login!", "error")

    return render_template("auth/login.html", form=form)



@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        return redirect(url_for("private.home"))
  
    else:
        flash("Erro no registro!", "error")

    return render_template("auth/register.html", form=form)