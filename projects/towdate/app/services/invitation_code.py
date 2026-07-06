def generate_invitation_code():
    """Compatibilidade para imports antigos."""

    from app.services.invitation_service import generate_invitation_code as _generate

    return _generate()
