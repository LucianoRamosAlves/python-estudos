from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.partner_forms import PartnerConnectForm, PartnerDisconnectForm
from app.private.routes import private
from app.services.relationship_service import (
    build_partner_context,
    connect_user_by_invitation_code,
    disconnect_partner,
)


def render_partner_page(connect_form, disconnect_form):
    return render_template(
        "private/accounts/partner.html",
        **build_partner_context(current_user, connect_form, disconnect_form),
    )


@private.route("/account/partner", methods=["GET", "POST"])
@login_required
def account_partner():
    connect_form = PartnerConnectForm()
    disconnect_form = PartnerDisconnectForm()

    form_type = request.form.get("form_type")

    if request.method == "POST":

        if form_type == "connect_partner":
            if not connect_form.validate_on_submit():
                flash("Corrija o código de convite informado.", "error")
                return render_partner_page(connect_form, disconnect_form)

            connection_error = connect_user_by_invitation_code(
                current_user,
                connect_form.partner_code.data,
            )

            if connection_error:
                connect_form.partner_code.errors.append(connection_error)
                flash(connection_error, "error")
                return render_partner_page(connect_form, disconnect_form)

            flash("Parceiro conectado com sucesso!", "success")
            return redirect(url_for("private.account_partner"))

        elif form_type == "disconnect_partner":

            if not disconnect_form.validate_on_submit():
                flash(
                    "Não foi possível validar a solicitação de desconexão.",
                    "error",
                )
                return render_partner_page(connect_form, disconnect_form)

            if not disconnect_partner(current_user):
                flash(
                    "Nenhum parceiro conectado para desconectar.",
                    "warning",
                )
                return redirect(url_for("private.account_partner"))

            flash("Parceiro desconectado com sucesso.", "success")
            return redirect(url_for("private.account_partner"))

    return render_partner_page(connect_form, disconnect_form)
