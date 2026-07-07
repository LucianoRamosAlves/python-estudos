from datetime import datetime

from app.extensions import db


class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer, db.ForeignKey("relationships.id"), nullable=False, index=True
    )

    code = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(40), nullable=False, default="outro")
    icon = db.Column(db.String(255), nullable=True)

    progress_current = db.Column(db.Integer, nullable=False, default=0)
    progress_goal = db.Column(db.Integer, nullable=False, default=1)

    unlocked = db.Column(db.Boolean, nullable=False, default=False, index=True)
    unlocked_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    relationship = db.relationship("Relationship", back_populates="achievements")

    def __repr__(self):
        return (
            f"<Achievement {self.code} ({'unlocked' if self.unlocked else 'locked'})>"
        )
