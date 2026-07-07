from datetime import date, datetime

from flask import url_for

from app.extensions import db
from app.models.calendar_event import CalendarEvent
from app.models.memory import Memory
from app.models.relationship import Relationship
from app.services.relationship_service import get_active_relationship_member


class CalendarServiceError(Exception):
    """Erro de negócio para o módulo de calendário."""


def _get_active_relationship(user):
    member = get_active_relationship_member(user)
    if member is None or member.relationship is None:
        return None
    return member.relationship


def _get_active_relationship_id(user):
    relationship = _get_active_relationship(user)
    if relationship is None:
        return None
    return relationship.id


def build_calendar_context(user, year=None, month=None):
    """Monta o contexto do calendário para o relacionamento ativo do usuário."""

    relationship = _get_active_relationship(user)
    if relationship is None:
        today = date.today()
        return {
            "year": today.year,
            "month": today.month,
            "month_name": today.strftime("%B"),
            "days": [],
            "events_by_day": {},
            "relationship": None,
            "selected_day": None,
            "selected_events": [],
        }

    today = date.today()
    target_year = int(year or today.year)
    target_month = int(month or today.month)

    if target_month < 1:
        target_month = 12
        target_year -= 1
    if target_month > 12:
        target_month = 1
        target_year += 1

    first_day = date(target_year, target_month, 1)
    days_in_month = (
        (
            date(target_year, target_month + 1, 1) - date(target_year, target_month, 1)
        ).days
        if target_month < 12
        else 31
    )
    if target_month == 12:
        days_in_month = 31 - first_day.day + 1

    calendar_days = []
    for day_number in range(1, days_in_month + 1):
        current_day = date(target_year, target_month, day_number)
        calendar_days.append(current_day)

    relationship_events = (
        CalendarEvent.query.filter_by(
            relationship_id=relationship.id,
        )
        .order_by(CalendarEvent.event_date.asc(), CalendarEvent.event_time.asc())
        .all()
    )

    memories = Memory.query.filter_by(
        relationship_id=relationship.id,
    ).all()

    events_by_day = {}
    for current_day in calendar_days:
        events = []
        for event in relationship_events:
            if event.event_date == current_day:
                events.append(
                    {
                        "id": event.id,
                        "title": event.title,
                        "description": event.description,
                        "time": event.event_time,
                        "location": event.location,
                        "category": event.category,
                        "favorite": event.favorite,
                        "source": "custom",
                    }
                )

        for memory in memories:
            if memory.memory_date == current_day:
                events.append(
                    {
                        "id": f"memory-{memory.id}",
                        "title": memory.title,
                        "description": memory.description,
                        "time": None,
                        "location": memory.location,
                        "category": "memory",
                        "favorite": memory.is_favorite,
                        "source": "memory",
                    }
                )

        if relationship.relationship_start_date == current_day:
            events.append(
                {
                    "id": "relationship-start",
                    "title": "Início do relacionamento",
                    "description": "Data especial do casal.",
                    "time": None,
                    "location": None,
                    "category": "relationship",
                    "favorite": True,
                    "source": "auto",
                }
            )

        if relationship.members:
            for member in relationship.members:
                if member.user and member.user.date_of_birth == current_day:
                    events.append(
                        {
                            "id": f"birthday-{member.user.id}",
                            "title": f"Aniversário de {member.user.full_name}",
                            "description": "Data especial do seu parceiro.",
                            "time": None,
                            "location": None,
                            "category": "birthday",
                            "favorite": True,
                            "source": "auto",
                        }
                    )

        if events:
            events_by_day[current_day.strftime("%Y-%m-%d")] = events

    selected_day = date(target_year, target_month, 1)
    selected_events = events_by_day.get(selected_day.strftime("%Y-%m-%d"), [])

    return {
        "year": target_year,
        "month": target_month,
        "month_name": first_day.strftime("%B"),
        "days": calendar_days,
        "events_by_day": events_by_day,
        "relationship": relationship,
        "selected_day": selected_day,
        "selected_events": selected_events,
    }


def create_event_for_relationship(user, form):
    """Cria um evento personalizado para o relacionamento ativo."""

    relationship_id = _get_active_relationship_id(user)
    if relationship_id is None:
        raise CalendarServiceError(
            "Você precisa ter um relacionamento ativo para criar eventos."
        )

    event = CalendarEvent(
        relationship_id=relationship_id,
        title=form.title.data.strip(),
        description=(form.description.data or "").strip() or None,
        event_date=form.event_date.data,
        event_time=(form.event_time.data or "").strip() or None,
        location=(form.location.data or "").strip() or None,
        category=form.category.data,
        favorite=bool(form.favorite.data),
    )

    db.session.add(event)
    db.session.commit()
    return event


def get_event_for_relationship(user, event_id):
    """Retorna um evento personalizado do relacionamento ativo."""

    relationship_id = _get_active_relationship_id(user)
    if relationship_id is None:
        return None

    return CalendarEvent.query.filter_by(
        relationship_id=relationship_id,
        id=event_id,
    ).first()


def update_event_for_relationship(user, event_id, form):
    """Atualiza um evento personalizado do relacionamento ativo."""

    event = get_event_for_relationship(user, event_id)
    if event is None:
        raise CalendarServiceError("Evento não encontrado.")

    event.title = form.title.data.strip()
    event.description = (form.description.data or "").strip() or None
    event.event_date = form.event_date.data
    event.event_time = (form.event_time.data or "").strip() or None
    event.location = (form.location.data or "").strip() or None
    event.category = form.category.data
    event.favorite = bool(form.favorite.data)

    db.session.commit()
    return event


def delete_event_for_relationship(user, event_id):
    """Exclui um evento personalizado do relacionamento ativo."""

    event = get_event_for_relationship(user, event_id)
    if event is None:
        raise CalendarServiceError("Evento não encontrado.")

    db.session.delete(event)
    db.session.commit()
