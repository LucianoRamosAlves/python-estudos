from flask import render_template
from flask_login import login_required, current_user

from app.private.routes import private
from app.services.achievement_service import get_achievements_for_relationship
from app.services.relationship_service import ensure_user_active_relationship


@private.route("/conquistas", methods=["GET"])
@login_required
def conquistas():
    """Página de conquistas do relacionamento ativo do usuário."""
    rel_member = ensure_user_active_relationship(current_user)
    relationship = rel_member.relationship if rel_member else None

    if relationship is None:
        achievements = []
    else:
        achievements = get_achievements_for_relationship(relationship)

    total = len(achievements)
    unlocked = sum(1 for a in achievements if a.unlocked)
    remaining = max(0, total - unlocked)
    percent = int((unlocked / total) * 100) if total else 0

    return render_template(
        "private/conquistas/conquistas.html",
        achievements=achievements,
        stats={
            "total": total,
            "unlocked": unlocked,
            "remaining": remaining,
            "percent": percent,
        },
    )
