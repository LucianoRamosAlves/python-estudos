from flask import jsonify, render_template, request, url_for
from flask_login import login_required, current_user

from app.private.routes import private
from app.forms.memory_map_forms import MemoryMapFilterForm
from app.services.memory_map_service import get_memories_for_map


@private.route("/memorias/mapa", methods=["GET"])
@login_required
def mapa_memorias():
    filter_form = MemoryMapFilterForm(request.args)

    # populate category choices from collections
    from app.models.memory_collection import MemoryCollection
    from app.services.relationship_service import ensure_user_active_relationship

    rel = ensure_user_active_relationship(current_user).relationship
    categories = [("", "Todas")] + [
        (c.slug, c.name)
        for c in MemoryCollection.query.filter_by(relationship_id=rel.id).all()
    ]
    filter_form.category.choices = categories

    return render_template("private/memorias/mapa.html", filter_form=filter_form)


@private.route("/memorias/mapa/data", methods=["GET"])
@login_required
def mapa_memorias_data():
    form = MemoryMapFilterForm(request.args)
    # parse filters
    category = form.category.data or None
    date_from = form.date_from.data or None
    date_to = form.date_to.data or None
    city = form.city.data or None
    favorites_only = bool(form.favorites_only.data)

    data = get_memories_for_map(
        current_user,
        category=category,
        date_from=date_from,
        date_to=date_to,
        city=city,
        favorites_only=favorites_only,
    )
    return jsonify(data)
