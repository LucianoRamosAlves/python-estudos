from app.extensions import db
from datetime import datetime


class User(db.Model):
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

    birth_date = db.Column(
        db.Date,
        nullable=True
    )

    avatar = db.Column(
        db.String(255),
        nullable=True,
        default="avatars/default.png"
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


    def __repr__(self):
        return f"<User {self.email}>"