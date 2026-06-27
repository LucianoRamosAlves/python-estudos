from app.extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)


    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    date_of_birth = db.Column(
        db.Date,
        nullable=True
    )

    avatar = db.Column(
        db.String(255),
        nullable=True,
        default="avatars/default.png"
    )

    cor_fundo = db.Column(
        db.String(7),
        nullable=True,
        default="#3b82f6"
    )

    cor_icone = db.Column(
        db.String(7),
        nullable=True,
        default="#3b82f6"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    session_version = db.Column(db.Integer, default=1, nullable=False)


    def __repr__(self):
        return f"<User {self.email}>"