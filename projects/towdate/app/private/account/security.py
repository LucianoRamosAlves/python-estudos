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

def update_password(user, new_password):
    user.password_hash = bcrypt.generate_password_hash(
        new_password
    ).decode("utf-8")

    user.session_version += 1

    db.session.commit()

def atualizar_senha(user, nova_senha):
    user.password_hash = bcrypt.generate_password_hash(
        nova_senha
    ).decode("utf-8")

    user.session_version += 1

    db.session.commit()


@private.route("/account/security", methods=["GET", "POST"])
@login_required
def account_security():

    form = ChangePasswordForm()
    logout_sessions_form = LogoutSessionsForm()
    delete_account_form = DeleteAccountForm()

    if form.validate_on_submit():

        if not bcrypt.check_password_hash(
            current_user.password_hash,
            form.senha_atual.data,
        ):
            form.senha_atual.errors.append("Senha atual incorreta.")
            flash("Senha atual incorreta.", "error")

            return render_template(
                "private/accounts/security.html",
                active_page="security",
                form=form,
                logout_sessions_form=logout_sessions_form,
                delete_account_form=delete_account_form,
            )

        atualizar_senha(current_user, form.nova_senha.data)

        session["session_version"] = current_user.session_version

        flash("Senha alterada com sucesso!", "success")

        return redirect(url_for("private.account_security"))

    elif form.is_submitted():
        flash("Corrija os erros do formulário.", "error")

    return render_template(
        "private/accounts/security.html",
        active_page="security",
        form=form,
        logout_sessions_form=logout_sessions_form,
        delete_account_form=delete_account_form,
    )