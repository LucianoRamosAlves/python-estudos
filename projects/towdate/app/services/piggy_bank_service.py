from datetime import datetime

from app.extensions import db
from app.models.piggy_bank import PiggyBank
from app.models.piggy_bank_movement import PiggyBankMovement
from app.services.relationship_service import ensure_user_active_relationship


class PiggyBankServiceError(Exception):
    """Exceção para erros de negócio do cofrinho."""


def _ensure_relationship_for_user(user):
    relationship_member = ensure_user_active_relationship(user)
    if relationship_member is None or relationship_member.relationship is None:
        raise PiggyBankServiceError(
            "Você precisa de um relacionamento ativo para gerenciar cofrinhos."
        )

    return relationship_member.relationship


def _normalize_status(target_amount, current_amount, status):
    if current_amount >= target_amount and target_amount > 0:
        return "completed"

    if status == "completed" and current_amount < target_amount:
        return "in_progress"

    if current_amount <= 0:
        return "planned"

    return status or "in_progress"


def get_piggy_bank_for_user(user, piggy_bank_id):
    """Busca um cofrinho do relacionamento do usuário."""
    relationship = _ensure_relationship_for_user(user)
    return PiggyBank.query.filter_by(
        id=piggy_bank_id, relationship_id=relationship.id
    ).first()


def get_piggy_banks_for_user(user):
    """Lista os cofrinhos do relacionamento do usuário."""
    relationship = _ensure_relationship_for_user(user)
    return (
        PiggyBank.query.filter_by(relationship_id=relationship.id)
        .order_by(PiggyBank.favorite.desc(), PiggyBank.created_at.desc())
        .all()
    )


def get_piggy_bank_dashboard_for_user(user):
    """Monta o resumo do dashboard do cofrinho."""
    relationship = _ensure_relationship_for_user(user)
    banks = PiggyBank.query.filter_by(relationship_id=relationship.id).all()

    if not banks:
        return {
            "total_saved": 0.0,
            "total_banks": 0,
            "completed_banks": 0,
            "average_progress": 0.0,
        }

    total_saved = round(sum(bank.current_amount for bank in banks), 2)
    completed_banks = sum(1 for bank in banks if bank.status == "completed")
    average_progress = round(
        sum(bank.progress_percentage for bank in banks) / len(banks),
        2,
    )

    return {
        "total_saved": total_saved,
        "total_banks": len(banks),
        "completed_banks": completed_banks,
        "average_progress": average_progress,
    }


def create_piggy_bank_for_user(user, form):
    """Cria um cofrinho para o relacionamento do usuário."""
    relationship = _ensure_relationship_for_user(user)

    piggy_bank = PiggyBank(
        relationship_id=relationship.id,
        title=form.title.data.strip(),
        description=form.description.data.strip() if form.description.data else None,
        target_amount=float(form.target_amount.data or 0),
        current_amount=float(form.current_amount.data or 0),
        category=form.category.data,
        target_date=form.target_date.data,
        status=_normalize_status(
            float(form.target_amount.data or 0),
            float(form.current_amount.data or 0),
            form.status.data,
        ),
        favorite=form.favorite.data,
    )

    db.session.add(piggy_bank)
    db.session.commit()
    return piggy_bank


def update_piggy_bank_for_user(user, piggy_bank_id, form):
    """Atualiza um cofrinho existente."""
    piggy_bank = get_piggy_bank_for_user(user, piggy_bank_id)
    if piggy_bank is None:
        raise PiggyBankServiceError("Cofrinho não encontrado.")

    piggy_bank.title = form.title.data.strip()
    piggy_bank.description = (
        form.description.data.strip() if form.description.data else None
    )
    piggy_bank.target_amount = float(form.target_amount.data or 0)
    piggy_bank.current_amount = float(form.current_amount.data or 0)
    piggy_bank.category = form.category.data
    piggy_bank.target_date = form.target_date.data
    piggy_bank.status = _normalize_status(
        piggy_bank.target_amount,
        piggy_bank.current_amount,
        form.status.data,
    )
    piggy_bank.favorite = form.favorite.data
    piggy_bank.updated_at = datetime.utcnow()

    db.session.commit()
    return piggy_bank


def delete_piggy_bank_for_user(user, piggy_bank_id):
    """Remove um cofrinho pertencente ao relacionamento do usuário."""
    piggy_bank = get_piggy_bank_for_user(user, piggy_bank_id)
    if piggy_bank is None:
        raise PiggyBankServiceError("Cofrinho não encontrado.")

    db.session.delete(piggy_bank)
    db.session.commit()


def add_movement_to_piggy_bank(user, piggy_bank_id, form):
    """Adiciona uma movimentação de depósito ao cofrinho e atualiza o saldo."""
    piggy_bank = get_piggy_bank_for_user(user, piggy_bank_id)
    if piggy_bank is None:
        raise PiggyBankServiceError("Cofrinho não encontrado.")

    movement = PiggyBankMovement(
        piggy_bank_id=piggy_bank.id,
        user_id=user.id,
        amount=float(form.amount.data or 0),
        observation=form.observation.data.strip() if form.observation.data else None,
    )

    db.session.add(movement)
    piggy_bank.current_amount = round(piggy_bank.current_amount + movement.amount, 2)
    piggy_bank.status = _normalize_status(
        piggy_bank.target_amount,
        piggy_bank.current_amount,
        piggy_bank.status,
    )
    piggy_bank.updated_at = datetime.utcnow()
    db.session.commit()
    return movement


def get_movements_for_piggy_bank(user, piggy_bank_id):
    """Lista o histórico de movimentações de um cofrinho."""
    piggy_bank = get_piggy_bank_for_user(user, piggy_bank_id)
    if piggy_bank is None:
        raise PiggyBankServiceError("Cofrinho não encontrado.")

    return (
        PiggyBankMovement.query.filter_by(piggy_bank_id=piggy_bank.id)
        .order_by(PiggyBankMovement.created_at.desc())
        .all()
    )
