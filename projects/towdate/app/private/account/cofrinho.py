from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.piggy_bank_forms import PiggyBankForm, PiggyBankMovementForm
from app.private.routes import private
from app.services.piggy_bank_service import (
    PiggyBankServiceError,
    add_movement_to_piggy_bank,
    create_piggy_bank_for_user,
    delete_piggy_bank_for_user,
    get_movements_for_piggy_bank,
    get_piggy_bank_dashboard_for_user,
    get_piggy_bank_for_user,
    get_piggy_banks_for_user,
    update_piggy_bank_for_user,
)


def _first_form_error(form):
    for errors in form.errors.values():
        if errors:
            return errors[0]
    return "Não foi possível validar o cofrinho."


@private.route("/cofrinho", methods=["GET", "POST"])
@login_required
def cofrinho():
    form = PiggyBankForm()

    if form.validate_on_submit():
        try:
            create_piggy_bank_for_user(current_user, form)
            flash("Cofrinho criado com sucesso!", "success")
            return redirect(url_for("private.cofrinho"))
        except PiggyBankServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("private.cofrinho"))

    if form.is_submitted():
        flash(_first_form_error(form), "error")
        return redirect(url_for("private.cofrinho"))

    piggy_banks = get_piggy_banks_for_user(current_user)
    dashboard = get_piggy_bank_dashboard_for_user(current_user)

    return render_template(
        "private/cofrinho/cofrinho.html",
        form=form,
        piggy_banks=piggy_banks,
        dashboard=dashboard,
    )


@private.route("/cofrinho/<int:piggy_bank_id>/editar", methods=["GET", "POST"])
@login_required
def editar_cofrinho(piggy_bank_id):
    piggy_bank = get_piggy_bank_for_user(current_user, piggy_bank_id)
    if piggy_bank is None:
        flash("Cofrinho não encontrado.", "error")
        return redirect(url_for("private.cofrinho"))

    form = PiggyBankForm()

    if form.validate_on_submit():
        try:
            update_piggy_bank_for_user(current_user, piggy_bank_id, form)
            flash("Cofrinho atualizado com sucesso!", "success")
            return redirect(url_for("private.cofrinho"))
        except PiggyBankServiceError as error:
            flash(str(error), "error")
            return redirect(
                url_for("private.editar_cofrinho", piggy_bank_id=piggy_bank_id)
            )

    if form.is_submitted():
        flash(_first_form_error(form), "error")

    if request.method == "GET":
        form.title.data = piggy_bank.title
        form.description.data = piggy_bank.description
        form.target_amount.data = piggy_bank.target_amount
        form.current_amount.data = piggy_bank.current_amount
        form.category.data = piggy_bank.category
        form.target_date.data = piggy_bank.target_date
        form.status.data = piggy_bank.status
        form.favorite.data = piggy_bank.favorite

    return render_template(
        "private/cofrinho/editar_cofrinho.html",
        form=form,
        piggy_bank=piggy_bank,
    )


@private.route("/cofrinho/<int:piggy_bank_id>/excluir", methods=["POST"])
@login_required
def excluir_cofrinho(piggy_bank_id):
    try:
        delete_piggy_bank_for_user(current_user, piggy_bank_id)
        flash("Cofrinho excluído com sucesso.", "success")
    except PiggyBankServiceError as error:
        flash(str(error), "error")

    return redirect(request.referrer or url_for("private.cofrinho"))


@private.route("/cofrinho/<int:piggy_bank_id>/movimento", methods=["POST"])
@login_required
def adicionar_movimento_cofrinho(piggy_bank_id):
    form = PiggyBankMovementForm()
    if form.validate_on_submit():
        try:
            add_movement_to_piggy_bank(current_user, piggy_bank_id, form)
            flash("Depósito registrado com sucesso.", "success")
        except PiggyBankServiceError as error:
            flash(str(error), "error")
    else:
        flash(_first_form_error(form), "error")

    return redirect(request.referrer or url_for("private.cofrinho"))


@private.route("/cofrinho/<int:piggy_bank_id>/historico")
@login_required
def historico_cofrinho(piggy_bank_id):
    piggy_bank = get_piggy_bank_for_user(current_user, piggy_bank_id)
    if piggy_bank is None:
        flash("Cofrinho não encontrado.", "error")
        return redirect(url_for("private.cofrinho"))

    movements = get_movements_for_piggy_bank(current_user, piggy_bank_id)

    return render_template(
        "private/cofrinho/historico.html",
        piggy_bank=piggy_bank,
        movements=movements,
    )
