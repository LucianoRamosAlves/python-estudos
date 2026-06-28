# app/public/routes.py

import email

from app.extensions import db, bcrypt
from flask import Blueprint, flash, render_template, session, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models.user import User

from app.auth.forms import (
    ChangePasswordForm,
    DeleteAccountForm,
    EditProfileForm,
    EditPhotoForm,
    LogoutSessionsForm,
)
from app.extensions import db
from app.services.upload_services import remover_foto_perfil, salvar_foto_perfil

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

        user = User.query.get(current_user.id)
        if current_user.avatar and current_user.avatar != "avatars/default.png":
            remover_foto_perfil(current_user.avatar)

        db.session.delete(user)
        db.session.commit()

        logout_user()
        session.clear()

        flash("Sua conta foi excluída com sucesso.", "success")

    return redirect(url_for("public.home"))


@private.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = EditProfileForm()
    photo_form = EditPhotoForm()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "photo":

            if photo_form.validate_on_submit():
                novo_nome = salvar_foto_perfil(photo_form.foto_perfil.data)
                if novo_nome:
                    current_user.avatar = novo_nome
                    db.session.commit()
                    flash("Foto de perfil atualizada com sucesso!", "success")
                    return redirect(url_for("private.account"))
                else:
                    flash("Erro ao atualizar a foto de perfil.", "error")
            else:
                flash("Erro ao atualizar a foto de perfil.", "error")
            return redirect(url_for("private.account"))

        elif form_type == "remove_photo":
            form_type = request.form.get("form_type")

            if (
                current_user.avatar == "avatars/default.png"
                or current_user.avatar is None
            ):
                flash("Nenhuma foto de perfil para remover.", "warning")
                return redirect(url_for("private.account"))

            if current_user.avatar:
                remover_foto_perfil(current_user.avatar)

                current_user.avatar = None

                db.session.commit()

                flash("Foto removida com sucesso!", "success")

            return redirect(url_for("private.account"))

        elif form_type == "profile":

            if form.validate_on_submit():
                if (
                    form.nome.data == current_user.first_name
                    and form.sobrenome.data == current_user.last_name
                    and form.email.data == current_user.email
                    and form.data_nascimento.data == current_user.date_of_birth
                ):
                    flash("Nenhuma alteração foi realizada.", "warning")
                    return redirect(url_for("private.account"))

                current_user.first_name = form.nome.data
                current_user.last_name = form.sobrenome.data
                current_user.email = form.email.data
                current_user.date_of_birth = form.data_nascimento.data

                db.session.commit()

                flash("Perfil atualizado com sucesso!", "success")
                return redirect(url_for("private.account"))

            flash("Erro ao atualizar o perfil.", "error")

    elif request.method == "GET":
        form.nome.data = current_user.first_name
        form.sobrenome.data = current_user.last_name
        form.email.data = current_user.email
        form.data_nascimento.data = current_user.date_of_birth

    return render_template(
        "private/accounts/account.html",
        active_page="account",
        form=form,
        photo_form=photo_form,
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
                "private/accounts/security.html", active_page="security", change_password_form=form, logout_sessions_form=logout_sessions_form, delete_account_form=delete_account_form
            )

        if form.nova_senha.data != form.confirmar_nova_senha.data:
            flash("As senhas não coincidem.", "error")
            form.confirmar_nova_senha.errors.append("As senhas não coincidem.")
            return render_template(
                "private/accounts/security.html", active_page="security", change_password_form=form, logout_sessions_form=logout_sessions_form, delete_account_form=delete_account_form
            )

        current_user.password_hash = bcrypt.generate_password_hash(
            form.nova_senha.data
        ).decode("utf-8")
        db.session.commit()

        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("private.account_security"))
    return render_template(
        "private/accounts/security.html",
        active_page="security",
        form=form,
        logout_sessions_form=logout_sessions_form,
        delete_account_form=delete_account_form,
    )


@private.route("/account/notifications")
@login_required
def account_notifications():
    return render_template(
        "private/accounts/notifications.html", active_page="notifications"
    )


@private.route("/account/preferences")
@login_required
def account_preferences():
    return render_template(
        "private/accounts/preferences.html", active_page="preferences"
    )
