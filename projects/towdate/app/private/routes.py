from flask import Blueprint

private = Blueprint("private", __name__)

from app.private.account import (
    home,
    logout_user,
    account,
    security,
    delete_account,
    notifications,
    preferences,
    relationship,
    partner,
)
