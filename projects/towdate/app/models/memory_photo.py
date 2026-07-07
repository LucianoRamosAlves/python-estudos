from datetime import datetime

from app.extensions import db


class MemoryPhoto(db.Model):
    __tablename__ = "memory_photos"

    id = db.Column(db.Integer, primary_key=True)

    memory_id = db.Column(
        db.Integer,
        db.ForeignKey("memories.id"),
        nullable=False,
        index=True,
    )

    image_path = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    memory = db.relationship(
        "Memory",
        back_populates="photos",
    )

    def __repr__(self):
        return f"<MemoryPhoto {self.id}>"
