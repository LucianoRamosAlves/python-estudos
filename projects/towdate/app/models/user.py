from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(id_user):
    return db.session.get(User, int(id_user))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    # identificador único do usuário
    id = db.Column(db.Integer, primary_key=True)

    # informações pessoais do usuário
    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    date_of_birth = db.Column(db.Date, nullable=True)

    # perfil do usuário
    avatar = db.Column(db.String(255), nullable=True, default=None)

    cor_fundo = db.Column(db.String(7), nullable=True, default="#3b82f6")

    cor_icone = db.Column(db.String(7), nullable=True, default="#3b82f6")

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    session_version = db.Column(db.Integer, default=1, nullable=False)

    relationships = db.relationship(
        "RelationshipMember",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True,
    )

    piggy_bank_movements = db.relationship(
        "PiggyBankMovement",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True,
    )

    # auditoria
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def username(self):
        if self.email:
            return self.email.split("@", 1)[0]
        return "usuario"

    # TODO futurante o email pode aparecer no logs, tenha cuidado ao usar esse método
    def __repr__(self):
        return f"<User {self.email}>"
