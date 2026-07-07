from datetime import datetime

from sqlalchemy import case

from app.extensions import db
from app.models.goal import Goal
from app.services.relationship_service import ensure_user_active_relationship


class GoalServiceError(Exception):
    pass


def _ensure_relationship_for_user(user):
    relationship_member = ensure_user_active_relationship(user)
    if relationship_member is None or relationship_member.relationship is None:
        raise GoalServiceError(
            "Você precisa de um relacionamento ativo para gerenciar metas."
        )

    return relationship_member.relationship


def _normalize_progress(value, status):
    progress = max(0, min(100, int(value or 0)))
    if progress >= 100:
        return 100, "completed"
    if progress <= 0:
        return 0, "planned"
    if status == "completed":
        return progress, "in_progress"
    return progress, status


def _priority_sort_expression():
    return case(
        (Goal.priority == "critical", 0),
        (Goal.priority == "high", 1),
        (Goal.priority == "medium", 2),
        (Goal.priority == "low", 3),
        else_=4,
    )


def get_goal_for_user(user, goal_id):
    relationship = _ensure_relationship_for_user(user)
    return Goal.query.filter_by(id=goal_id, relationship_id=relationship.id).first()


def get_goals_for_user(
    user, category=None, status=None, sort_by="priority", sort_order="desc"
):
    relationship = _ensure_relationship_for_user(user)
    query = Goal.query.filter_by(relationship_id=relationship.id)

    if category:
        query = query.filter(Goal.category == category)

    if status:
        query = query.filter(Goal.status == status)

    if sort_by == "target_date":
        if sort_order == "asc":
            query = query.order_by(
                Goal.target_date.is_(None),
                Goal.target_date.asc(),
                Goal.created_at.desc(),
            )
        else:
            query = query.order_by(
                Goal.target_date.is_(None),
                Goal.target_date.desc(),
                Goal.created_at.desc(),
            )
    else:
        if sort_order == "asc":
            query = query.order_by(
                Goal.favorite.desc(),
                _priority_sort_expression().asc(),
                Goal.target_date.asc().nullsfirst(),
                Goal.created_at.desc(),
            )
        else:
            query = query.order_by(
                Goal.favorite.desc(),
                _priority_sort_expression().asc(),
                Goal.target_date.asc().nullsfirst(),
                Goal.created_at.desc(),
            )

    return query.all()


def create_goal_for_user(user, form):
    relationship = _ensure_relationship_for_user(user)

    progress, status = _normalize_progress(form.progress.data, form.status.data)

    goal = Goal(
        relationship_id=relationship.id,
        title=form.title.data.strip(),
        description=form.description.data.strip() if form.description.data else None,
        category=form.category.data,
        priority=form.priority.data,
        status=status,
        progress=progress,
        target_date=form.target_date.data,
        favorite=form.favorite.data,
    )

    db.session.add(goal)
    db.session.commit()
    return goal


def update_goal_for_user(user, goal_id, form):
    goal = get_goal_for_user(user, goal_id)
    if goal is None:
        raise GoalServiceError("Meta não encontrada.")

    progress, status = _normalize_progress(form.progress.data, form.status.data)

    goal.title = form.title.data.strip()
    goal.description = form.description.data.strip() if form.description.data else None
    goal.category = form.category.data
    goal.priority = form.priority.data
    goal.status = status
    goal.progress = progress
    goal.target_date = form.target_date.data
    goal.favorite = form.favorite.data
    goal.updated_at = datetime.utcnow()

    db.session.commit()
    return goal


def delete_goal_for_user(user, goal_id):
    goal = get_goal_for_user(user, goal_id)
    if goal is None:
        raise GoalServiceError("Meta não encontrada.")

    db.session.delete(goal)
    db.session.commit()


def complete_goal_for_user(user, goal_id):
    goal = get_goal_for_user(user, goal_id)
    if goal is None:
        raise GoalServiceError("Meta não encontrada.")

    goal.progress = 100
    goal.status = "completed"
    goal.updated_at = datetime.utcnow()
    db.session.commit()
    return goal


def update_goal_progress_for_user(user, goal_id, progress):
    goal = get_goal_for_user(user, goal_id)
    if goal is None:
        raise GoalServiceError("Meta não encontrada.")

    normalized_progress, status = _normalize_progress(progress, goal.status)
    goal.progress = normalized_progress
    goal.status = status
    goal.updated_at = datetime.utcnow()
    db.session.commit()
    return goal
