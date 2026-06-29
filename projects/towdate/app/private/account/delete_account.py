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



@private.route("/account/delete", methods=["POST"])
@login_required
def delete_account():
    change_password_form = ChangePasswordForm()
    logout_sessions_form = LogoutSessionsForm()
    form = DeleteAccountForm()


    if form.validate_on_submit():
        check_password = bcrypt.check_password_hash(
            current_user.password_hash, form.senha.data
        )
        if not check_password:
            flash("Senha atual incorreta.", "error")
            form.senha.errors.append("Senha atual incorreta.")
            return render_template(
                "private/accounts/security.html",
                active_page="security",
                form=change_password_form,
                logout_sessions_form=logout_sessions_form,
                delete_account_form=form,
            )

        user = db.session.get(User, current_user.id)

        if current_user.avatar and current_user.avatar != "avatars/default.svg":
            remover_foto_perfil(current_user.avatar)

        db.session.delete(user)
        db.session.commit()

        logout_user()
        session.clear()

        flash("Sua conta foi excluída com sucesso.", "success")

    if not form.validate_on_submit():
        flash("Erro", "error")
        return redirect(url_for("private.account_security"))

    return redirect(url_for("public.home"))