from datetime import datetime

from app.extensions import db


class PiggyBankMovement(db.Model):
    """Representa uma movimentação de depósito em um cofrinho."""

    __tablename__ = "piggy_bank_movements"

    id = db.Column(db.Integer, primary_key=True)

    piggy_bank_id = db.Column(
        db.Integer,
        db.ForeignKey("piggy_banks.id"),
        nullable=False,
        index=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    amount = db.Column(db.Float, nullable=False)
    observation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    piggy_bank = db.relationship("PiggyBank", back_populates="movements")
    user = db.relationship("User", back_populates="piggy_bank_movements")

    def __repr__(self):
        return f"<PiggyBankMovement {self.id}>"
