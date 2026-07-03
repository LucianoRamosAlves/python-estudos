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

def atualizar_perfil(user, form):
    user.first_name = form.nome.data
    user.last_name = form.sobrenome.data
    user.email = form.email.data
    user.date_of_birth = form.data_nascimento.data

def preencher_formulario(form, user):
    form.nome.data = user.first_name
    form.sobrenome.data = user.last_name
    form.email.data = user.email
    form.data_nascimento.data = user.date_of_birth

def atualizar_foto_perfil(user, novo_nome):
    user.avatar = novo_nome
    db.session.commit()


def remover_avatar(user):
    if not user.avatar:
        return False

    remover_foto_perfil(user.avatar)

    user.avatar = None

    db.session.commit()

    return True

@private.route("/account", methods=["GET", "POST"])
@login_required
def account():

    form = EditProfileForm()
    photo_form = EditPhotoForm()

    if request.method == "POST":

        form_type = request.form.get("form_type")

        if form_type == "photo":

            if not photo_form.validate_on_submit():
                flash("Erro ao atualizar a foto de perfil.", "error")
                return redirect(url_for("private.account"))

            novo_nome = salvar_foto_perfil(photo_form.foto_perfil.data)

            if not novo_nome:
                flash("Erro ao atualizar a foto de perfil.", "error")
                return redirect(url_for("private.account"))

            atualizar_foto_perfil(current_user, novo_nome)

            flash("Foto de perfil atualizada com sucesso!", "success")
            return redirect(url_for("private.account"))

        elif form_type == "remove_photo":

            if not remover_avatar(current_user):
                flash("Nenhuma foto de perfil para remover.", "warning")
            else:
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

                atualizar_perfil(current_user, form)

                db.session.commit()

                flash("Perfil atualizado com sucesso!", "success")
                return redirect(url_for("private.account"))

            flash("Erro ao atualizar o perfil.", "error")

    else:
        preencher_formulario(form, current_user)

    return render_template(
        "private/accounts/account.html",
        active_page="account",
        form=form,
        photo_form=photo_form,
    )