from datetime import datetime

from app.extensions import db


class MemoryCollection(db.Model):
    __tablename__ = "memory_collections"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False)

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
        back_populates="memory_collections",
    )

    memories = db.relationship(
        "Memory",
        back_populates="collection",
        cascade="all, delete-orphan",
        lazy=True,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "relationship_id",
            "slug",
            name="uq_memory_collection_relationship_slug",
        ),
    )

    def __repr__(self):
        return f"<MemoryCollection {self.slug}>"
