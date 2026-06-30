import os
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.private.routes import private


@private.route("/account/relationship", methods=["GET", "POST"])
@login_required
def account_relationship():
    relationship_status = session.get("relationship_status", "💖 Namorando")
    relationship_date = session.get("relationship_date", "")
    couple_name = session.get("couple_name", "")
    relationship_phrase = session.get("relationship_phrase", "")
    couple_photo = session.get("couple_photo", "")

    if request.method == "POST":
        relationship_status = request.form.get(
            "relationship_status", relationship_status
        )
        relationship_date = request.form.get("relationship_date", "")
        couple_name = request.form.get("couple_name", "")
        relationship_phrase = request.form.get("relationship_phrase", "")

        uploaded_file = request.files.get("couple_photo")
        if uploaded_file and uploaded_file.filename:
            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "couples",
            )
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(upload_folder, filename))
            couple_photo = filename

        session["relationship_status"] = relationship_status
        session["relationship_date"] = relationship_date
        session["couple_name"] = couple_name
        session["relationship_phrase"] = relationship_phrase
        session["couple_photo"] = couple_photo

        flash("Informações do relacionamento atualizadas com sucesso!", "success")
        return redirect(url_for("private.account_relationship"))

    return render_template(
        "private/accounts/relationship.html",
        active_page="relationship",
        relationship_status=relationship_status,
        relationship_date=relationship_date,
        couple_name=couple_name,
        relationship_phrase=relationship_phrase,
        couple_photo=couple_photo,
    )
