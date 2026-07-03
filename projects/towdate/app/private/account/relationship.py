

from app.forms.relationship_forms import RelationshipForm
from flask import (
    flash,
    render_template,
    url_for,
    request,
    redirect,
)
from flask_login import current_user, login_required
from app.extensions import db

from app.private.routes import private
from app.models.relationship import Relationship
from app.models.relationship_member import RelationshipMember


@private.route("/account/relationship", methods=["GET", "POST"])
@login_required
def account_relationship():

    form = RelationshipForm()

    member = current_user.relationships[0] if current_user.relationships else None
    relationship = member.relationship if member else None

    # Preenche o formulário ao abrir a página
    if relationship and not form.is_submitted():
        form.relationship_status.data = relationship.relationship_status
        form.relationship_phrase.data = relationship.relationship_phrase
        form.relationship_start_date.data = relationship.relationship_start_date

    if form.validate_on_submit():

        if relationship is None:

            relationship = Relationship(
                relationship_status=form.relationship_status.data,
                relationship_phrase=form.relationship_phrase.data,
                relationship_start_date=form.relationship_start_date.data,
            )

            db.session.add(relationship)
            db.session.flush()

            member = RelationshipMember(
                relationship_id=relationship.id,
                user_id=current_user.id,
            )

            db.session.add(member)

        else:

            relationship.relationship_status = form.relationship_status.data
            relationship.relationship_phrase = form.relationship_phrase.data
            relationship.relationship_start_date = form.relationship_start_date.data

        db.session.commit()

        flash("Relacionamento salvo com sucesso.", "success")
        return redirect(url_for("private.account_relationship"))

    return render_template(
        "private/accounts/relationship.html",
        form=form,
        relationship=relationship,
    )

