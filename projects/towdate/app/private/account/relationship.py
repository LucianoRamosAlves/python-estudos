

from app.forms.relationship_forms import RelationshipForm
from flask import (
    flash,
    render_template,
)
from flask_login import current_user, login_required
from app.extensions import db

from app.private.routes import private
from app.models.relationship import Relationship


@private.route("/account/relationship", methods=["GET", "POST"])
@login_required
def account_relationship():
    form = RelationshipForm()
    
    if form.validate_on_submit():
        relationship = Relationship(
        relationship_status=form.relationship_status.data,
        relationship_phrase=form.relationship_phrase.data,
        relationship_start_date=form.relationship_start_date.data,
    )
        db.session.add(relationship)
        db.session.commit()
        flash("Relacionamento atualizado com sucesso.", "success")
    return render_template(
        "private/accounts/relationship.html",
        form=form
    )

