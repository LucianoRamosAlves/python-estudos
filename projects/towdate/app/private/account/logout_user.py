from flask import flash, redirect, session, url_for
from flask_login import current_user, login_required, logout_user

from app.extensions import db
from app.auth.forms import LogoutSessionsForm
from app.private.routes import private

@private.route("/sair")
@login_required
def sair():
    logout_user()
    return redirect(url_for("public.home"))


@private.route("/account/logout-sessions", methods=["POST"])
@login_required
def logout_sessions():
    form = LogoutSessionsForm()

    if form.validate_on_submit():

        current_user.session_version += 1
        db.session.commit()

        session["session_version"] = current_user.session_version

        flash("Todas as sessões foram encerradas com sucesso.", "success")

    return redirect(url_for("private.account_security"))