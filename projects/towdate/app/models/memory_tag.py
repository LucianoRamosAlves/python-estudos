from datetime import datetime

from app.extensions import db


class MemoryTag(db.Model):
    __tablename__ = "memory_tags"

    id = db.Column(db.Integer, primary_key=True)

    memory_id = db.Column(
        db.Integer,
        db.ForeignKey("memories.id"),
        nullable=False,
        index=True,
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        nullable=False,
        index=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    memory = db.relationship(
        "Memory",
        back_populates="memory_tags",
    )

    tag = db.relationship(
        "Tag",
        back_populates="memory_tags",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "memory_id",
            "tag_id",
            name="uq_memory_tag_memory_tag",
        ),
    )

    def __repr__(self):
        return f"<MemoryTag memory={self.memory_id} tag={self.tag_id}>"
