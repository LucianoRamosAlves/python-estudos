from flask import render_template

from flask_login import login_required

from app.private.routes import private



@private.route("/account/notifications")
@login_required
def account_notifications():
    return render_template(
        "private/accounts/notifications.html", active_page="notifications"
    )