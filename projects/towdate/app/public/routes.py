# app/public/routes.py

from flask import Blueprint, render_template, url_for

public = Blueprint("public", __name__)

@public.route("/")
def home():
    return render_template("public/components/home.html")