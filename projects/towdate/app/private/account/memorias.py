from flask import render_template
from flask_login import login_required

from app.private.routes import private


@private.route("/memorias")
@login_required
def memorias():
    return render_template("private/memorias/memorias.html")
