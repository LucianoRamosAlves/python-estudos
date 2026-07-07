from datetime import datetime

from app.extensions import db


class Wish(db.Model):
    __tablename__ = "wishes"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer, db.ForeignKey("relationships.id"), nullable=False, index=True
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(40), nullable=False, default="outro")
    priority = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(20), nullable=False, default="pending")
    favorite = db.Column(db.Boolean, nullable=False, default=False)
    link = db.Column(db.String(255), nullable=True)
    price_estimated = db.Column(db.Numeric(10, 2), nullable=True)
    planned_date = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    relationship = db.relationship("Relationship", back_populates="wishes")

    def __repr__(self):
        return f"<Wish {self.id} {self.title}>"
