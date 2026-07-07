from datetime import datetime

from app.extensions import db


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(40), nullable=False, default="casal")
    priority = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(20), nullable=False, default="planned")
    progress = db.Column(db.Integer, nullable=False, default=0)
    target_date = db.Column(db.Date, nullable=True)
    favorite = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    relationship = db.relationship(
        "Relationship",
        back_populates="goals",
    )

    def __repr__(self):
        return f"<Goal {self.id}>"
