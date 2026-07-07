from datetime import datetime

from app.extensions import db


class CalendarEvent(db.Model):
    __tablename__ = "calendar_events"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=False, index=True)
    event_time = db.Column(db.String(10), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(40), nullable=False, default="personal")
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
        back_populates="calendar_events",
    )

    def __repr__(self):
        return f"<CalendarEvent {self.id}>"
