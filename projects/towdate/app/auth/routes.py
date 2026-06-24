
from flask import Blueprint, render_template, url_for

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("auth/login.html")