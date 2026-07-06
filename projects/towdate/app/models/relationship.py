from datetime import datetime

from app.extensions import db


class Relationship(db.Model):
    __tablename__ = "relationships"

    id = db.Column(db.Integer, primary_key=True)

    relationship_status = db.Column(db.String(30), nullable=False, default="Namorando")

    relationship_phrase = db.Column(db.String(255), nullable=True)

    couple_photo = db.Column(
        db.String(255),
        nullable=False,
        default="couples/default.jpg",
    )

    relationship_start_date = db.Column(db.Date, nullable=False)

    relationship_end_date = db.Column(db.Date, nullable=True)

    relationship_is_active = db.Column(db.Boolean, default=True, nullable=False)

    invitation_code = db.Column(db.String(20), unique=True, nullable=True, index=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    members = db.relationship(
        "RelationshipMember",
        back_populates="relationship",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Relationship {self.id}>"