import secrets
import string

from app.models.relationship import Relationship

ALPHABET = string.ascii_uppercase + string.digits
CODE_LENGTH = 20


def normalize_invitation_code(code):
    """Normaliza o código removendo separadores e padronizando em maiúsculo."""

    if code is None:
        return ""

    return code.replace("-", "").replace(" ", "").strip().upper()


def generate_invitation_code():
    """Gera um código de convite único."""

    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))

        exists = Relationship.query.filter_by(invitation_code=code).first()
        if exists is None:
            return code
