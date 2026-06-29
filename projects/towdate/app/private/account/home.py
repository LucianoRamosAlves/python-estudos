from flask import render_template
from flask_login import login_required

from app.private.routes import private


@private.route("/home")
@login_required
def home():
    return render_template("private/home/home.html")