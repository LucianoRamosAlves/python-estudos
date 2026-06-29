from flask import render_template

from flask_login import login_required

from app.private.routes import private

@private.route("/account/preferences")
@login_required
def account_preferences():
    return render_template(
        "private/accounts/preferences.html", active_page="preferences"
    )