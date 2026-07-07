from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.memory_forms import MemoryCreateForm, MemoryDeleteForm, MemoryUpdateForm
from app.private.routes import private
from app.services.memory_service import (
    MemoryServiceError,
    apply_memory_form_defaults,
    create_memory_for_user,
    get_memory_for_user,
    get_memories_dashboard_context_for_user,
    update_memory_for_user,
    delete_memory_for_user,
)


def _first_form_error(form):
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Nao foi possivel validar os dados da memoria."


@private.route("/memorias", methods=["GET", "POST"])
@login_required
def memorias():
    form = MemoryCreateForm()
    apply_memory_form_defaults(form)

    if form.validate_on_submit():
        try:
            create_memory_for_user(current_user, form)
            flash("Memoria registrada com sucesso!", "success")
            return redirect(url_for("private.memorias"))
        except MemoryServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.memorias"))

    if form.is_submitted():
        flash(_first_form_error(form), "error")
        return redirect(url_for("private.memorias"))

    dashboard = get_memories_dashboard_context_for_user(current_user)

    return render_template(
        "private/memorias/memorias.html",
        memory_form=form,
        dashboard=dashboard,
    )


def _populate_update_form(form, memory):
    form.title.data = memory.title
    form.description.data = memory.description
    form.memory_date.data = memory.memory_date
    form.location.data = memory.location or ""
    form.collection_slug.data = memory.collection.slug if memory.collection else ""
    form.custom_collection_name.data = ""
    form.tags.data = ", ".join(item.tag.name for item in memory.memory_tags)
    form.rating.data = memory.rating
    form.favorite.data = memory.is_favorite


@private.route("/memorias/<int:memory_id>/editar", methods=["GET", "POST"])
@login_required
def editar_memoria(memory_id):
    memory = get_memory_for_user(current_user, memory_id)
    if memory is None:
        flash("Memoria nao encontrada.", "error")
        return redirect(url_for("private.memorias"))

    form = MemoryUpdateForm()

    if form.validate_on_submit():
        try:
            update_memory_for_user(current_user, memory_id, form)
            flash("Memoria atualizada com sucesso!", "success")
            return redirect(
                url_for("private.colecao", collection_slug=form.collection_slug.data)
            )
        except MemoryServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.editar_memoria", memory_id=memory_id))

    if form.is_submitted():
        flash(_first_form_error(form), "error")

    if request.method == "GET":
        _populate_update_form(form, memory)

    return render_template(
        "private/memorias/editar_memoria.html",
        form=form,
        memory=memory,
    )


@private.route("/memorias/<int:memory_id>/excluir", methods=["POST"])
@login_required
def excluir_memoria(memory_id):
    form = MemoryDeleteForm()
    fallback = request.referrer or url_for("private.memorias")

    if not form.validate_on_submit():
        flash("Solicitacao invalida para exclusao de memoria.", "error")
        return redirect(fallback)

    try:
        delete_memory_for_user(current_user, memory_id)
        flash("Memoria excluida com sucesso.", "success")
    except MemoryServiceError as error:
        flash(str(error), "error")

    return redirect(fallback)
