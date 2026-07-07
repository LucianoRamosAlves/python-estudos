from flask import render_template, request
from flask_login import current_user, login_required

from app.forms.memory_forms import MemoryDeleteForm
from app.private.routes import private
from app.services.memory_service import get_collection_context_for_user_filtered


@private.route("/memorias/colecao/<collection_slug>")
@login_required
def colecao(collection_slug):
    query = request.args.get("q", "").strip()
    date_filter = request.args.get("date_filter", "all").strip() or "all"
    sort = request.args.get("sort", "recent").strip() or "recent"

    collection = get_collection_context_for_user_filtered(
        current_user,
        collection_slug,
        query=query,
        date_filter=date_filter,
        sort=sort,
    )

    delete_form = MemoryDeleteForm()

    return render_template(
        "private/memorias/colecao.html",
        collection=collection,
        delete_form=delete_form,
    )
