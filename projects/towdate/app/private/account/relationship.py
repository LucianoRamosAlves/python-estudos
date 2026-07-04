
from app.forms.relationship_forms import (
    EndRelationshipForm,
    RelationshipForm,
    RelationshipPhotoForm,
)
from flask import (
    flash,
    render_template,
    url_for,
    request,
    redirect,
)
from flask_login import current_user, login_required
from app.extensions import bcrypt, db

from app.private.routes import private
from app.models.relationship import Relationship
from app.models.relationship_member import RelationshipMember
from app.services.upload_services import salvar_foto_casal, remover_foto_casal

def preencher_formulario_relacionamento(form, relationship):
    form.relationship_status.data = relationship.relationship_status
    form.relationship_phrase.data = relationship.relationship_phrase
    form.relationship_start_date.data = relationship.relationship_start_date

def atualizar_relacionamento(relationship, form):
    relationship.relationship_status = form.relationship_status.data
    relationship.relationship_phrase = form.relationship_phrase.data
    relationship.relationship_start_date = form.relationship_start_date.data

def obter_relacionamento_atual(user):
    member = user.relationships[0] if user.relationships else None
    return member.relationship if member else None

def encerrar_relacionamento(relationship, password):
    if not bcrypt.check_password_hash(current_user.password_hash, password):
        return False

    if relationship.couple_photo:
        remover_foto_casal(relationship.couple_photo)

    db.session.delete(relationship)
    db.session.commit()

    return True




@private.route("/account/relationship", methods=["GET", "POST"])
@login_required
def account_relationship():

    form = RelationshipForm()
    photo_form = RelationshipPhotoForm()
    end_relationship_form = EndRelationshipForm()
    form_type = request.form.get("form_type")

    relationship = obter_relacionamento_atual(current_user)

    if relationship and not form.is_submitted():
        preencher_formulario_relacionamento(form, relationship)

    if request.method == "POST":

        if form_type == "photo":

            if not photo_form.validate_on_submit():
                if relationship:
                    preencher_formulario_relacionamento(form, relationship)
                flash("Erro ao atualizar a foto do casal.", "error")
                return render_template(
                    "private/accounts/relationship.html",
                    active_page="relationship",
                    form=form,
                    photo_form=photo_form,
                    end_relationship_form=end_relationship_form,
                    relationship=relationship,
                )

            if relationship is None:
                    flash("Você ainda não possui um relacionamento registrado. Preencha os campos abaixo para criar um.", "warning")
                    return render_template(
                        "private/accounts/relationship.html",
                        active_page="relationship",
                        form=form,
                        photo_form=photo_form,
                        end_relationship_form=end_relationship_form,
                        relationship=relationship,
                    )

            if not photo_form.couple_photo.data:
                flash("Selecione uma imagem para atualizar a foto do casal.", "warning")
                return redirect(url_for("private.account_relationship"))

            novo_nome = salvar_foto_casal(photo_form.couple_photo.data)

            if not novo_nome:
                flash("Erro ao enviar a foto.", "error")
                return redirect(url_for("private.account_relationship"))

            # remover foto antiga, se existir
            if relationship.couple_photo:
                remover_foto_casal(relationship.couple_photo)

            relationship.couple_photo = novo_nome

            db.session.commit()

            flash("Foto do casal atualizada com sucesso.", "success")

            return redirect(url_for("private.account_relationship"))

        elif form_type == "relationship":

            if form.validate_on_submit():

                if relationship is None:

                    relationship = Relationship(
                        relationship_status=form.relationship_status.data,
                        relationship_phrase=form.relationship_phrase.data,
                        relationship_start_date=form.relationship_start_date.data,
                    )

                    db.session.add(relationship)
                    db.session.flush()

                    member = RelationshipMember(
                        relationship_id=relationship.id,
                        user_id=current_user.id,
                    )

                    db.session.add(member)

                else:

                    atualizar_relacionamento(relationship, form)

                db.session.commit()

                flash("Relacionamento salvo com sucesso.", "success")
                return redirect(url_for("private.account_relationship"))

            else:
                flash("Erro ao salvar o relacionamento. Verifique os campos.", "error")

        elif form_type == "end_relationship":

            if relationship is None:
                flash("Nenhum relacionamento encontrado para encerrar.", "warning")
                return redirect(url_for("private.account_relationship"))

            if not end_relationship_form.validate_on_submit():
                if relationship:
                    preencher_formulario_relacionamento(form, relationship)
                flash("Informe sua senha para encerrar o relacionamento.", "error")
                return render_template(
                    "private/accounts/relationship.html",
                    active_page="relationship",
                    form=form,
                    photo_form=photo_form,
                    end_relationship_form=end_relationship_form,
                    relationship=relationship,
                )

            if not encerrar_relacionamento(relationship, end_relationship_form.password.data):
                end_relationship_form.password.errors.append("Senha incorreta.")
                preencher_formulario_relacionamento(form, relationship)
                flash("Senha incorreta.", "error")
                return render_template(
                    "private/accounts/relationship.html",
                    active_page="relationship",
                    form=form,
                    photo_form=photo_form,
                    end_relationship_form=end_relationship_form,
                    relationship=relationship,
                )

            flash("Relacionamento encerrado com sucesso.", "success")
            return redirect(url_for("private.account_relationship"))

    return render_template(
        "private/accounts/relationship.html",
        active_page="relationship",
        form=form,
        photo_form=photo_form,
        end_relationship_form=end_relationship_form,
        relationship=relationship,
    )