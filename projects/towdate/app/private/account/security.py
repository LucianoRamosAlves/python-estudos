from flask import (
    flash,
    redirect,
    render_template,
    session,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

from app.private.routes import private

from app.extensions import (
    db,
    bcrypt,
)

from app.auth.forms import (
    ChangePasswordForm,
    DeleteAccountForm,
    LogoutSessionsForm,
)

@private.route("/account/security", methods=["GET", "POST"])
@login_required
def account_security():
    form = ChangePasswordForm()
    logout_sessions_form = LogoutSessionsForm()
    delete_account_form = DeleteAccountForm()

    if form.validate_on_submit():
        check_password = bcrypt.check_password_hash(
            current_user.password_hash, form.senha_atual.data
        )
        if not check_password:
            flash("Senha atual incorreta.", "error")
            form.senha_atual.errors.append("Senha atual incorreta.")
            return render_template(
                "private/accounts/security.html", active_page="security", form=form, logout_sessions_form=logout_sessions_form, delete_account_form=delete_account_form
            )

        elif form.nova_senha.data != form.confirmar_nova_senha.data:
            flash("As senhas não coincidem.", "error")
            form.confirmar_nova_senha.errors.append("As senhas não coincidem.")
            return render_template(
                "private/accounts/security.html", active_page="security", form=form, logout_sessions_form=logout_sessions_form, delete_account_form=delete_account_form
            )


        current_user.password_hash = bcrypt.generate_password_hash(
            form.nova_senha.data
        ).decode("utf-8")

        current_user.session_version += 1
        db.session.commit()

        session["session_version"] = current_user.session_version

        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("private.account_security"))

    elif form.is_submitted() and not form.validate():
        flash("Erro ao alterar a senha.", "error")


    return render_template(
        "private/accounts/security.html",
        active_page="security",
        form=form,
        logout_sessions_form=logout_sessions_form,
        delete_account_form=delete_account_form,
    )