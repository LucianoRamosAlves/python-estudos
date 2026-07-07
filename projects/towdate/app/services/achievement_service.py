"""Service to manage relationship achievements.

All business rules for unlocking achievements live here.
"""

from datetime import date, datetime

from app.extensions import db
from app.models.achievement import Achievement
from app.models.relationship import Relationship
from app.models.memory import Memory
from app.models.memory_photo import MemoryPhoto
from app.models.calendar_event import CalendarEvent
from app.models.goal import Goal
from app.models.piggy_bank import PiggyBank
from app.models.wish import Wish

ACHIEVEMENT_DEFINITIONS = [
    # Relationship milestones
    {
        "code": "rel_1_day",
        "title": "Primeiro dia juntos",
        "desc": "Comemorou o primeiro dia juntos.",
        "category": "Relacionamento",
        "metric": "days_together",
        "goal": 1,
        "icon": "icons/rel_day.svg",
    },
    {
        "code": "rel_100_days",
        "title": "100 dias juntos",
        "desc": "100 dias de história a dois.",
        "category": "Relacionamento",
        "metric": "days_together",
        "goal": 100,
        "icon": "icons/rel_100.svg",
    },
    {
        "code": "rel_1_year",
        "title": "1 ano juntos",
        "desc": "Um ano celebrando o amor.",
        "category": "Relacionamento",
        "metric": "days_together",
        "goal": 365,
        "icon": "icons/rel_1y.svg",
    },
    {
        "code": "rel_2_years",
        "title": "2 anos juntos",
        "desc": "Duas voltas ao redor do sol juntos.",
        "category": "Relacionamento",
        "metric": "days_together",
        "goal": 365 * 2,
        "icon": "icons/rel_2y.svg",
    },
    {
        "code": "rel_5_years",
        "title": "5 anos juntos",
        "desc": "Cinco anos de parceria.",
        "category": "Relacionamento",
        "metric": "days_together",
        "goal": 365 * 5,
        "icon": "icons/rel_5y.svg",
    },
    # Memories
    {
        "code": "mem_1",
        "title": "Primeira memória",
        "desc": "Registrou a primeira memória.",
        "category": "Memórias",
        "metric": "memories_count",
        "goal": 1,
        "icon": "icons/mem_1.svg",
    },
    {
        "code": "mem_10",
        "title": "10 memórias",
        "desc": "Dez memórias compartilhadas.",
        "category": "Memórias",
        "metric": "memories_count",
        "goal": 10,
        "icon": "icons/mem_10.svg",
    },
    {
        "code": "mem_50",
        "title": "50 memórias",
        "desc": "Cinquenta memórias criadas.",
        "category": "Memórias",
        "metric": "memories_count",
        "goal": 50,
        "icon": "icons/mem_50.svg",
    },
    {
        "code": "mem_100",
        "title": "100 memórias",
        "desc": "Cem momentos inesquecíveis.",
        "category": "Memórias",
        "metric": "memories_count",
        "goal": 100,
        "icon": "icons/mem_100.svg",
    },
    # Photos
    {
        "code": "photo_1",
        "title": "Primeira foto",
        "desc": "Adicionou a primeira foto.",
        "category": "Fotos",
        "metric": "photos_count",
        "goal": 1,
        "icon": "icons/photo_1.svg",
    },
    {
        "code": "photo_50",
        "title": "50 fotos",
        "desc": "Cinquenta fotos no álbum.",
        "category": "Fotos",
        "metric": "photos_count",
        "goal": 50,
        "icon": "icons/photo_50.svg",
    },
    {
        "code": "photo_100",
        "title": "100 fotos",
        "desc": "Cem fotos registradas.",
        "category": "Fotos",
        "metric": "photos_count",
        "goal": 100,
        "icon": "icons/photo_100.svg",
    },
    # Calendar
    {
        "code": "cal_event_1",
        "title": "Primeiro evento",
        "desc": "Criou o primeiro evento no calendário.",
        "category": "Calendário",
        "metric": "calendar_events_count",
        "goal": 1,
        "icon": "icons/cal_1.svg",
    },
    {
        "code": "cal_event_10",
        "title": "10 eventos",
        "desc": "Dez eventos registrados.",
        "category": "Calendário",
        "metric": "calendar_events_count",
        "goal": 10,
        "icon": "icons/cal_10.svg",
    },
    # Goals
    {
        "code": "goal_1",
        "title": "Primeira meta criada",
        "desc": "Criou a primeira meta.",
        "category": "Metas",
        "metric": "goals_count",
        "goal": 1,
        "icon": "icons/goal_1.svg",
    },
    {
        "code": "goal_completed_1",
        "title": "Primeira meta concluída",
        "desc": "Concluiu a primeira meta.",
        "category": "Metas",
        "metric": "goals_completed",
        "goal": 1,
        "icon": "icons/goal_done_1.svg",
    },
    {
        "code": "goal_completed_10",
        "title": "10 metas concluídas",
        "desc": "Dez metas concluídas.",
        "category": "Metas",
        "metric": "goals_completed",
        "goal": 10,
        "icon": "icons/goal_done_10.svg",
    },
    # Piggy bank
    {
        "code": "piggy_1",
        "title": "Primeiro cofrinho",
        "desc": "Criou o primeiro cofrinho.",
        "category": "Cofrinho",
        "metric": "piggy_banks_count",
        "goal": 1,
        "icon": "icons/piggy_1.svg",
    },
    {
        "code": "piggy_goal_done_1",
        "title": "Primeira meta financeira concluída",
        "desc": "Concluiu a primeira meta financeira.",
        "category": "Cofrinho",
        "metric": "piggy_banks_completed",
        "goal": 1,
        "icon": "icons/piggy_done_1.svg",
    },
    # Wishes
    {
        "code": "wish_1",
        "title": "Primeiro desejo",
        "desc": "Cadastrou o primeiro desejo.",
        "category": "Lista de desejos",
        "metric": "wishes_count",
        "goal": 1,
        "icon": "icons/wish_1.svg",
    },
    {
        "code": "wish_25",
        "title": "25 desejos cadastrados",
        "desc": "Vinte e cinco desejos registrados.",
        "category": "Lista de desejos",
        "metric": "wishes_count",
        "goal": 25,
        "icon": "icons/wish_25.svg",
    },
    # Map locations
    {
        "code": "loc_1",
        "title": "Primeiro local visitado",
        "desc": "Registrou o primeiro local no mapa.",
        "category": "Mapa",
        "metric": "distinct_locations",
        "goal": 1,
        "icon": "icons/loc_1.svg",
    },
    {
        "code": "loc_10",
        "title": "10 locais diferentes",
        "desc": "Dez locais distintos visitados.",
        "category": "Mapa",
        "metric": "distinct_locations",
        "goal": 10,
        "icon": "icons/loc_10.svg",
    },
    {
        "code": "loc_50",
        "title": "50 locais diferentes",
        "desc": "Cinquenta locais distintos.",
        "category": "Mapa",
        "metric": "distinct_locations",
        "goal": 50,
        "icon": "icons/loc_50.svg",
    },
]


def _compute_metrics(relationship: Relationship):
    """Compute relevant numeric metrics for the given relationship.

    Returns a dict with metric names used by ACHIEVEMENT_DEFINITIONS.
    """
    today = date.today()
    metrics = {}

    # Days together
    try:
        start = relationship.relationship_start_date
        days = (today - start).days if start else 0
        metrics["days_together"] = max(0, days)
    except Exception:
        metrics["days_together"] = 0

    # Counts from DB
    metrics["memories_count"] = Memory.query.filter_by(
        relationship_id=relationship.id
    ).count()

    # photos count
    photos = (
        db.session.query(db.func.count(MemoryPhoto.id))
        .join(Memory, Memory.id == MemoryPhoto.memory_id)
        .filter(Memory.relationship_id == relationship.id)
        .scalar()
        or 0
    )
    metrics["photos_count"] = int(photos)

    metrics["calendar_events_count"] = CalendarEvent.query.filter_by(
        relationship_id=relationship.id
    ).count()

    metrics["goals_count"] = Goal.query.filter_by(
        relationship_id=relationship.id
    ).count()
    metrics["goals_completed"] = Goal.query.filter_by(
        relationship_id=relationship.id, status="completed"
    ).count()

    metrics["piggy_banks_count"] = PiggyBank.query.filter_by(
        relationship_id=relationship.id
    ).count()
    metrics["piggy_banks_completed"] = PiggyBank.query.filter_by(
        relationship_id=relationship.id, status="completed"
    ).count()

    metrics["wishes_count"] = Wish.query.filter_by(
        relationship_id=relationship.id
    ).count()

    # distinct locations (city)
    distinct = (
        db.session.query(db.func.count(db.func.distinct(Memory.city)))
        .filter(Memory.relationship_id == relationship.id)
        .filter(Memory.city.isnot(None))
        .scalar()
        or 0
    )
    metrics["distinct_locations"] = int(distinct)

    return metrics


def sync_achievements_for_relationship(relationship: Relationship):
    """Ensure achievement rows exist and update progress/unlock state.

    Returns list of Achievement instances for the relationship.
    """
    if relationship is None:
        return []

    metrics = _compute_metrics(relationship)
    results = []

    try:
        for definition in ACHIEVEMENT_DEFINITIONS:
            code = definition["code"]
            metric = definition["metric"]
            goal = int(definition.get("goal", 1))

            ach = Achievement.query.filter_by(
                relationship_id=relationship.id, code=code
            ).first()
            if ach is None:
                ach = Achievement(
                    relationship_id=relationship.id,
                    code=code,
                    title=definition.get("title") or code,
                    description=definition.get("desc") or "",
                    category=definition.get("category") or "outro",
                    icon=definition.get("icon"),
                    progress_current=0,
                    progress_goal=goal,
                    unlocked=False,
                )
                db.session.add(ach)

            current = int(metrics.get(metric, 0))
            ach.progress_current = current
            ach.progress_goal = goal

            if not ach.unlocked and current >= goal:
                ach.unlocked = True
                ach.unlocked_at = datetime.utcnow()

            results.append(ach)

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return results


def get_achievements_for_relationship(relationship: Relationship):
    """Return achievements for UI display, ensuring sync before returning."""
    sync_achievements_for_relationship(relationship)
    return (
        Achievement.query.filter_by(relationship_id=relationship.id)
        .order_by(
            Achievement.unlocked.desc(),
            Achievement.unlocked_at.desc().nullslast(),
            Achievement.title,
        )
        .all()
    )
