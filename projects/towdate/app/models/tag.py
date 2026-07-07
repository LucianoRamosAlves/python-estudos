from datetime import datetime

from app.extensions import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False, index=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    memory_tags = db.relationship(
        "MemoryTag",
        back_populates="tag",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
