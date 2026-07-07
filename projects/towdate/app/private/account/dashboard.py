from flask import render_template
from flask_login import login_required, current_user

from app.private.routes import private
from app.services.dashboard_service import get_dashboard_for_user


@private.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Renderiza o dashboard do casal para o usuário autenticado."""
    context = get_dashboard_for_user(current_user)
    return render_template("private/dashboard/dashboard.html", **context)
