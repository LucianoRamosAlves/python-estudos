# app/public/routes.py

from flask import Blueprint, render_template, url_for, redirect, flash, get_flashed_messages

private = Blueprint("private", __name__)

@private.route("/home")
def home():
    return render_template("private/home/home.html")