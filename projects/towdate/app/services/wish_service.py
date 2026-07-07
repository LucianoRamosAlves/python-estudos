from datetime import datetime

from app.extensions import db
from app.models.wish import Wish
from app.services.relationship_service import ensure_user_active_relationship


class WishServiceError(Exception):
    pass


def _ensure_relationship_for_user(user):
    relationship_member = ensure_user_active_relationship(user)
    if relationship_member is None or relationship_member.relationship is None:
        raise WishServiceError(
            "Você precisa de um relacionamento ativo para gerenciar desejos."
        )

    return relationship_member.relationship


def get_wish_for_user(user, wish_id):
    relationship = _ensure_relationship_for_user(user)
    return Wish.query.filter_by(id=wish_id, relationship_id=relationship.id).first()


def get_wishes_for_user(
    user, category=None, status=None, sort_by="created_at", sort_order="desc", q=None
):
    relationship = _ensure_relationship_for_user(user)
    query = Wish.query.filter_by(relationship_id=relationship.id)

    if category:
        query = query.filter(Wish.category == category)

    if status:
        query = query.filter(Wish.status == status)

    if q:
        term = f"%{q}%"
        query = query.filter((Wish.title.ilike(term)) | (Wish.description.ilike(term)))

    if sort_by == "planned_date":
        if sort_order == "asc":
            query = query.order_by(
                Wish.planned_date.is_(None),
                Wish.planned_date.asc(),
                Wish.created_at.desc(),
            )
        else:
            query = query.order_by(
                Wish.planned_date.is_(None),
                Wish.planned_date.desc(),
                Wish.created_at.desc(),
            )
    else:
        if sort_order == "asc":
            query = query.order_by(Wish.created_at.asc())
        else:
            query = query.order_by(Wish.created_at.desc())

    return query.all()


def create_wish_for_user(user, form):
    relationship = _ensure_relationship_for_user(user)

    wish = Wish(
        relationship_id=relationship.id,
        title=form.title.data.strip(),
        description=form.description.data.strip() if form.description.data else None,
        category=form.category.data,
        priority=form.priority.data,
        status=form.status.data,
        favorite=form.favorite.data,
        link=form.link.data.strip() if form.link.data else None,
        price_estimated=form.price_estimated.data,
        planned_date=form.planned_date.data,
    )

    db.session.add(wish)
    db.session.commit()
    return wish


def update_wish_for_user(user, wish_id, form):
    wish = get_wish_for_user(user, wish_id)
    if wish is None:
        raise WishServiceError("Desejo não encontrado.")

    wish.title = form.title.data.strip()
    wish.description = form.description.data.strip() if form.description.data else None
    wish.category = form.category.data
    wish.priority = form.priority.data
    wish.status = form.status.data
    wish.favorite = form.favorite.data
    wish.link = form.link.data.strip() if form.link.data else None
    wish.price_estimated = form.price_estimated.data
    wish.planned_date = form.planned_date.data
    wish.updated_at = datetime.utcnow()

    db.session.commit()
    return wish


def delete_wish_for_user(user, wish_id):
    wish = get_wish_for_user(user, wish_id)
    if wish is None:
        raise WishServiceError("Desejo não encontrado.")

    db.session.delete(wish)
    db.session.commit()


def toggle_favorite_for_user(user, wish_id):
    wish = get_wish_for_user(user, wish_id)
    if wish is None:
        raise WishServiceError("Desejo não encontrado.")

    wish.favorite = not bool(wish.favorite)
    wish.updated_at = datetime.utcnow()
    db.session.commit()
    return wish


def complete_wish_for_user(user, wish_id):
    wish = get_wish_for_user(user, wish_id)
    if wish is None:
        raise WishServiceError("Desejo não encontrado.")

    wish.status = "completed"
    wish.updated_at = datetime.utcnow()
    db.session.commit()
    return wish
