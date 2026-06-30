from app.extensions import db
from datetime import datetime


class Couples(db.Model):
    __tablename__ = "couples"

    id = db.Column(db.Integer, primary_key=True)

    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    relationship_date = db.Column(db.Date, nullable=True)

    relationship_status = db.Column(db.String(30), nullable=False, default="Namorando")

    couple_photo = db.Column(
        db.String(255), nullable=True, default="couples/default.jpg"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relacionamentos com a tabela de usuários
    user1 = db.relationship("User", foreign_keys=[user1_id], lazy=True)

    user2 = db.relationship("User", foreign_keys=[user2_id], lazy=True)

    def __repr__(self):
        return f"<Couple {self.user1_id} - {self.user2_id}>"
