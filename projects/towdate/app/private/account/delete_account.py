from flask import flash, redirect, render_template, session, url_for

from flask_login import current_user, login_required, logout_user

from app.private.routes import private

from app.extensions import db, bcrypt

from app.models.user import User

from app.auth.forms import (
    ChangePasswordForm,
    DeleteAccountForm,
    LogoutSessionsForm,
)

from app.services.upload_services import remover_foto_perfil

def excluir_conta(user):

    if user.avatar:
        remover_foto_perfil(user.avatar)

    db.session.delete(user)
    db.session.commit()

@private.route("/account/delete", methods=["POST"])
@login_required
def delete_account():

    change_password_form = ChangePasswordForm()
    logout_sessions_form = LogoutSessionsForm()
    form = DeleteAccountForm()

    if not form.validate_on_submit():
        flash("Erro ao excluir a conta.", "error")
        return redirect(url_for("private.account_security"))

    if not bcrypt.check_password_hash(
        current_user.password_hash,
        form.senha.data,
    ):

        form.senha.errors.append("Senha atual incorreta.")
        flash("Senha atual incorreta.", "error")

        return render_template(
            "private/accounts/security.html",
            active_page="security",
            form=change_password_form,
            logout_sessions_form=logout_sessions_form,
            delete_account_form=form,
        )

    excluir_conta(current_user)

    logout_user()
    session.clear()

    flash("Sua conta foi excluída com sucesso.", "success")

    return redirect(url_for("public.home"))