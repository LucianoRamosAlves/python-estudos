from datetime import datetime

from app.extensions import db


class Memory(db.Model):
    __tablename__ = "memories"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
        index=True,
    )

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("memory_collections.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    memory_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(120), nullable=True)

    rating = db.Column(db.Integer, nullable=False)
    is_favorite = db.Column(db.Boolean, nullable=False, default=False)

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

    relationship = db.relationship(
        "Relationship",
        back_populates="memories",
    )

    collection = db.relationship(
        "MemoryCollection",
        back_populates="memories",
    )

    photos = db.relationship(
        "MemoryPhoto",
        back_populates="memory",
        cascade="all, delete-orphan",
        lazy=True,
    )

    memory_tags = db.relationship(
        "MemoryTag",
        back_populates="memory",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Memory {self.id}>"
