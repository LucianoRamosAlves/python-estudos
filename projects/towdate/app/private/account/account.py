from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import current_user, login_required

from app.private.routes import private

from app.extensions import db

from app.auth.forms import (
    EditPhotoForm,
    EditProfileForm,
)

from app.services.upload_services import (
    remover_foto_perfil,
    salvar_foto_perfil,
)


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

        elif form_type == "remove_photo":
            form_type = request.form.get("form_type")

            if (
                current_user.avatar == "avatars/default.svg"
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
