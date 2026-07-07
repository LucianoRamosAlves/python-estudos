"""Dashboard service: agregação de métricas e itens para o painel do casal.

Fornece funções públicas para obter o contexto necessário na tela do Dashboard.
"""
from datetime import date, datetime, timedelta
from typing import List, Dict

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.relationship import Relationship
from app.models.memory import Memory
from app.models.memory_photo import MemoryPhoto
from app.models.calendar_event import CalendarEvent
from app.models.goal import Goal
from app.models.piggy_bank import PiggyBank
from app.models.wish import Wish
from app.models.achievement import Achievement
from app.services.relationship_service import ensure_user_active_relationship


def _next_occurrence_of_month_day(month: int, day: int, from_date: date) -> date:
    """Retorna a próxima ocorrência de (month, day) a partir de from_date (inclusive)."""
    year = from_date.year
    try:
        candidate = date(year, month, day)
    except Exception:
        # invalid day (feb 29), fallback to 28
        candidate = date(year, month, min(day, 28))

    if candidate < from_date:
        year += 1
        try:
            candidate = date(year, month, day)
        except Exception:
            candidate = date(year, month, min(day, 28))

    return candidate


def _next_birthday(dob: date, from_date: date) -> date:
    if dob is None:
        return None
    return _next_occurrence_of_month_day(dob.month, dob.day, from_date)


def _next_anniversary(start_date: date, from_date: date) -> date:
    if start_date is None:
        return None
    return _next_occurrence_of_month_day(start_date.month, start_date.day, from_date)


def get_dashboard_for_user(user) -> Dict:
    """Gera o contexto do Dashboard para o `user` logado.

    Retorna um dict pronto para passar ao template.
    """
    member = ensure_user_active_relationship(user)
    relationship = member.relationship if member else None

    if relationship is None:
        return {"relationship": None}

    rel_id = relationship.id
    today = date.today()

    # header
    days_together = (today - relationship.relationship_start_date).days if relationship.relationship_start_date else 0

    # stats
    memories_count = Memory.query.filter_by(relationship_id=rel_id).count()

    photos_count = (
        db.session.query(func.count(MemoryPhoto.id))
        .join(Memory, Memory.id == MemoryPhoto.memory_id)
        .filter(Memory.relationship_id == rel_id)
        .scalar()
        or 0
    )

    # events this month
    start_month = date(today.year, today.month, 1)
    end_month = (start_month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    events_month = (
        CalendarEvent.query.filter(
            CalendarEvent.relationship_id == rel_id,
            CalendarEvent.event_date >= start_month,
            CalendarEvent.event_date <= end_month,
        ).count()
    )

    active_goals = Goal.query.filter(Goal.relationship_id == rel_id, Goal.status != "completed").count()

    active_piggy = PiggyBank.query.filter(PiggyBank.relationship_id == rel_id, PiggyBank.status != "completed").count()

    wishes_pending = Wish.query.filter(Wish.relationship_id == rel_id, Wish.status != "realizado").count()

    achievements_unlocked = Achievement.query.filter(Achievement.relationship_id == rel_id, Achievement.unlocked == True).count()

    # next events: calendar events + birthdays + anniversary
    upcoming: List[Dict] = []

    # calendar events
    cal_events = (
        CalendarEvent.query.filter(CalendarEvent.relationship_id == rel_id, CalendarEvent.event_date >= today)
        .order_by(CalendarEvent.event_date.asc())
        .limit(8)
        .all()
    )
    for ev in cal_events:
        upcoming.append({"type": "event", "title": ev.title, "date": ev.event_date, "source": ev})

    # birthdays
    for m in relationship.members:
        dob = getattr(m.user, "date_of_birth", None)
        next_b = _next_birthday(dob, today) if dob else None
        if next_b:
            upcoming.append({"type": "birthday", "title": m.user.full_name, "date": next_b, "source": m.user})

    # relationship anniversary
    ann = _next_anniversary(relationship.relationship_start_date, today)
    if ann:
        upcoming.append({"type": "anniversary", "title": "Aniversário do relacionamento", "date": ann, "source": relationship})

    upcoming_sorted = sorted(upcoming, key=lambda x: x["date"])[:8]

    # last memories (avoid N+1)
    last_memories = (
        Memory.query.options(joinedload(Memory.photos))
        .filter(Memory.relationship_id == rel_id)
        .order_by(Memory.created_at.desc())
        .limit(6)
        .all()
    )

    # goals in progress
    goals = (
        Goal.query.filter(Goal.relationship_id == rel_id)
        .order_by(Goal.updated_at.desc())
        .limit(6)
        .all()
    )

    # piggy banks
    piggies = (
        PiggyBank.query.filter(PiggyBank.relationship_id == rel_id)
        .order_by(PiggyBank.updated_at.desc())
        .limit(6)
        .all()
    )

    # wishes
    wishes = (
        Wish.query.filter(Wish.relationship_id == rel_id)
        .order_by(Wish.created_at.desc())
        .limit(6)
        .all()
    )

    # achievements latest unlocked
    achievements = (
        Achievement.query.filter(Achievement.relationship_id == rel_id, Achievement.unlocked == True)
        .order_by(Achievement.unlocked_at.desc())
        .limit(6)
        .all()
    )

    stats = {
        "days_together": days_together,
        "memories": memories_count,
        "photos": int(photos_count),
        "events_month": events_month,
        "goals_active": active_goals,
        "piggy_active": active_piggy,
        "wishes_pending": wishes_pending,
        "achievements_unlocked": achievements_unlocked,
    }

    header = {
        "photo": relationship.couple_photo,
        "phrase": relationship.relationship_phrase,
        "status": relationship.relationship_status,
        "days_together": days_together,
        "start_date": relationship.relationship_start_date,
    }

    return {
        "relationship": header,
        "stats": stats,
        "upcoming": upcoming_sorted,
        "last_memories": last_memories,
        "goals": goals,
        "piggies": piggies,
        "wishes": wishes,
        "achievements": achievements,
    }
