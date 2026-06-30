from flask import render_template
from flask_login import login_required

from app.private.routes import private


@private.route("/account/partner")
@login_required
def account_partner():
    return render_template(
        "private/accounts/partner.html",
        active_page="partner",
        partner_name="Andréia",
        partner_status="connected",
        partner_avatar=None,
        pending_request=False,
        invite_code="ABCD-1234",
        connected_since="12 Junho 2026",
    )
