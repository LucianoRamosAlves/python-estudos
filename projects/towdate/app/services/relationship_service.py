from datetime import date, datetime

from app.extensions import db
from app.models.relationship import Relationship
from app.models.relationship_member import RelationshipMember
from app.services.invitation_service import (
    generate_invitation_code,
    normalize_invitation_code,
)


def get_active_relationship_member(user):
    """Retorna o membro mais recente de um relacionamento ativo do usuário."""

    members = sorted(
        user.relationships,
        key=lambda member: member.joined_at or datetime.min,
        reverse=True,
    )

    for member in members:
        if member.relationship and member.relationship.relationship_is_active:
            return member

    return None


def get_active_relationship_id(user):
    """Retorna o id do relationship ativo do usuário autenticado."""

    member = get_active_relationship_member(user)
    if member is None or member.relationship is None:
        return None

    return member.relationship.id


def get_connected_partner(user):
    """Retorna o parceiro conectado e o membro correspondente no relacionamento."""

    current_member = get_active_relationship_member(user)
    if current_member is None:
        return None, None

    for relationship_member in current_member.relationship.members:
        if relationship_member.user_id != user.id:
            return relationship_member.user, relationship_member

    return None, current_member


def get_relationship_owner(relationship):
    """Retorna o primeiro membro que entrou no relacionamento."""

    if relationship is None or not relationship.members:
        return None

    owner_member = min(relationship.members, key=lambda member: member.joined_at)
    return owner_member.user


def create_base_relationship():
    """Cria um relacionamento ativo inicial com código de convite."""

    relationship = Relationship(
        relationship_status="namorando",
        relationship_start_date=date.today(),
        invitation_code=generate_invitation_code(),
    )
    db.session.add(relationship)
    db.session.flush()
    return relationship


def ensure_relationship_invitation_code(relationship):
    """Garante que o relacionamento possua invitation_code."""

    if relationship is None:
        return None

    if relationship.invitation_code:
        return relationship.invitation_code

    try:
        relationship.invitation_code = generate_invitation_code()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return None

    return relationship.invitation_code


def ensure_user_active_relationship(user):
    """Garante relacionamento ativo para o usuário da tela de parceiro."""

    relationship_member = get_active_relationship_member(user)
    if relationship_member is not None:
        return relationship_member

    try:
        relationship = create_base_relationship()
        relationship_member = RelationshipMember(
            relationship_id=relationship.id,
            user_id=user.id,
        )
        db.session.add(relationship_member)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return None

    return relationship_member


def find_relationship_by_invitation_code(code):
    """Localiza e valida um relacionamento pelo código de convite."""

    normalized_code = normalize_invitation_code(code)

    relationship = Relationship.query.filter_by(invitation_code=normalized_code).first()
    if relationship is None:
        return None, "Código de convite inválido."

    if not relationship.relationship_is_active:
        return None, "Este relacionamento não está mais ativo."

    if len(relationship.members) == 0:
        return None, "Este convite é inválido."

    if len(relationship.members) >= 2:
        return None, "Este código de convite já foi utilizado."

    return relationship, None


def _validate_user_can_join_relationship(current_user, relationship):
    owner = get_relationship_owner(relationship)
    if owner is None:
        return "Não foi possível localizar o proprietário do convite."

    if owner.id == current_user.id:
        return "Você não pode conectar a própria conta."

    current_partner, current_member = get_connected_partner(current_user)
    if current_partner is not None:
        return "Você já possui um parceiro conectado."

    if current_member is not None:
        if current_member.relationship_id == relationship.id:
            return "Você já participa deste relacionamento."

        if _is_user_solo_relationship_member(current_member, current_user.id):
            return None

        return "Você já participa de um relacionamento e não pode se conectar sem perder dados existentes."

    return None


def _is_user_solo_relationship_member(relationship_member, user_id):
    """Verifica se o membro pertence a um relacionamento ativo só com o próprio usuário."""

    if relationship_member is None:
        return False

    relationship = relationship_member.relationship
    if relationship is None or not relationship.relationship_is_active:
        return False

    members = relationship.members or []
    return len(members) == 1 and members[0].user_id == user_id


def connect_user_by_invitation_code(current_user, code):
    """Conecta o usuário ao relacionamento encontrado pelo código de convite."""

    relationship, invite_error = find_relationship_by_invitation_code(code)
    if invite_error:
        return invite_error

    validation_error = _validate_user_can_join_relationship(current_user, relationship)
    if validation_error:
        return validation_error

    try:
        current_member = get_active_relationship_member(current_user)
        if (
            current_member is not None
            and current_member.relationship_id != relationship.id
            and _is_user_solo_relationship_member(current_member, current_user.id)
        ):
            previous_relationship = current_member.relationship
            db.session.delete(current_member)
            db.session.delete(previous_relationship)

        db.session.add(
            RelationshipMember(
                relationship_id=relationship.id,
                user_id=current_user.id,
            )
        )
        relationship.invitation_code = generate_invitation_code()
        db.session.commit()
    except Exception:
        db.session.rollback()
        return "Não foi possível conectar o parceiro neste momento."

    return None


def disconnect_partner(user):
    """Desconecta o parceiro atual do relacionamento ativo do usuário."""

    partner, partner_member = get_connected_partner(user)
    if partner is None or partner_member is None or partner_member.user_id == user.id:
        return False

    try:
        db.session.delete(partner_member)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True


def format_date_ptbr(value):
    if value is None:
        return None

    months = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro",
    }

    raw_date = value.date() if isinstance(value, datetime) else value
    return f"{raw_date.day} de {months[raw_date.month]} de {raw_date.year}"


def build_partner_context(user, connect_form, disconnect_form):
    """Monta o contexto da tela de parceiro."""

    partner, partner_member = get_connected_partner(user)
    relationship_member = ensure_user_active_relationship(user)
    relationship = relationship_member.relationship if relationship_member else None
    invite_code = ensure_relationship_invitation_code(relationship)

    connected_since_source = None
    if partner is not None and partner_member is not None:
        if partner_member.joined_at is not None:
            connected_since_source = partner_member.joined_at
        elif relationship is not None:
            connected_since_source = relationship.created_at

    return {
        "active_page": "partner",
        "connect_form": connect_form,
        "disconnect_form": disconnect_form,
        "current_user_name": user.first_name,
        "partner_name": partner.full_name if partner else None,
        "partner_avatar": partner.avatar if partner else None,
        "partner_status": "connected" if partner else "disconnected",
        "pending_request": False,
        "invite_code": invite_code,
        "connected_since": format_date_ptbr(connected_since_source),
        "is_connected": partner is not None,
        "can_connect": partner is None,
    }
