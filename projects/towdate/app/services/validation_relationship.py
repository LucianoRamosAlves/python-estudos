from app.extensions import db

from app.relationship.models import Relationship
from app.relationship_member.models import RelationshipMember

from app.services.invitation_service import generate_invitation_code


def create_relationship(user, relationship_start_date):
    """
    Cria um relacionamento e adiciona o usuário como primeiro membro.
    """

    # Validação: usuário deve existir
    if user is None:
        raise ValueError("Usuário inválido.")

    # Validação: usuário precisa estar salvo no banco
    if user.id is None:
        raise ValueError("Usuário não encontrado.")

    # Validação: não pode participar de outro relacionamento
    if user.relationships:
        raise ValueError(
            "Você já participa de um relacionamento."
        )

    # Validação: data obrigatória
    if relationship_start_date is None:
        raise ValueError(
            "Informe a data de início do relacionamento."
        )

    relationship = Relationship(
        relationship_start_date=relationship_start_date,
        invitation_code=generate_invitation_code(),
    )

    db.session.add(relationship)
    db.session.flush()

    member = RelationshipMember(
        relationship_id=relationship.id,
        user_id=user.id,
    )

    db.session.add(member)
    db.session.commit()

    return relationship