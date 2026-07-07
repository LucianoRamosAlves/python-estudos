from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.wish_forms import WishForm, WishFilterForm
from app.private.routes import private
from app.services.wish_service import (
    WishServiceError,
    complete_wish_for_user,
    create_wish_for_user,
    delete_wish_for_user,
    get_wish_for_user,
    get_wishes_for_user,
    toggle_favorite_for_user,
    update_wish_for_user,
)


def _first_form_error(form):
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Não foi possível validar o desejo."


@private.route("/desejos", methods=["GET", "POST"])
@login_required
def desejos():
    form = WishForm()
    filter_form = WishFilterForm(request.args)

    if form.validate_on_submit():
        try:
            create_wish_for_user(current_user, form)
            flash("Desejo criado com sucesso!", "success")
            return redirect(url_for("private.desejos"))
        except WishServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.desejos"))

    if form.is_submitted():
        flash(_first_form_error(form), "error")
        return redirect(url_for("private.desejos"))

    wishes = get_wishes_for_user(
        current_user,
        category=filter_form.category.data or None,
        status=filter_form.status.data or None,
        sort_by=filter_form.sort_by.data or "created_at",
        sort_order=filter_form.order.data or "desc",
        q=request.args.get("q") or None,
    )

    return render_template(
        "private/desejos/desejos.html",
        form=form,
        filter_form=filter_form,
        wishes=wishes,
    )


@private.route("/desejos/<int:wish_id>/editar", methods=["GET", "POST"])
@login_required
def editar_desejo(wish_id):
    wish = get_wish_for_user(current_user, wish_id)
    if wish is None:
        flash("Desejo não encontrado.", "error")
        return redirect(url_for("private.desejos"))

    form = WishForm()

    if form.validate_on_submit():
        try:
            update_wish_for_user(current_user, wish_id, form)
            flash("Desejo atualizado com sucesso!", "success")
            return redirect(url_for("private.desejos"))
        except WishServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.editar_desejo", wish_id=wish_id))

    if form.is_submitted():
        flash(_first_form_error(form), "error")

    if request.method == "GET":
        form.title.data = wish.title
        form.description.data = wish.description
        form.category.data = wish.category
        form.priority.data = wish.priority
        form.status.data = wish.status
        form.favorite.data = wish.favorite
        form.link.data = wish.link
        form.price_estimated.data = wish.price_estimated
        form.planned_date.data = wish.planned_date

    return render_template("private/desejos/editar_desejo.html", form=form, wish=wish)


@private.route("/desejos/<int:wish_id>/excluir", methods=["POST"])
@login_required
def excluir_desejo(wish_id):
    try:
        delete_wish_for_user(current_user, wish_id)
        flash("Desejo excluído com sucesso.", "success")
    except WishServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.desejos"))


@private.route("/desejos/<int:wish_id>/favorito", methods=["POST"])
@login_required
def favorito_desejo(wish_id):
    try:
        toggle_favorite_for_user(current_user, wish_id)
        flash("Favorito atualizado.", "success")
    except WishServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.desejos"))


@private.route("/desejos/<int:wish_id>/realizar", methods=["POST"])
@login_required
def realizar_desejo(wish_id):
    try:
        complete_wish_for_user(current_user, wish_id)
        flash("Desejo marcado como realizado.", "success")
    except WishServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.desejos"))
