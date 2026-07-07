from datetime import datetime

from app.extensions import db


class PiggyBank(db.Model):
    """Representa um cofrinho pertencente a um relacionamento."""

    __tablename__ = "piggy_banks"

    id = db.Column(db.Integer, primary_key=True)

    relationship_id = db.Column(
        db.Integer,
        db.ForeignKey("relationships.id"),
        nullable=False,
        index=True,
    )

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    target_amount = db.Column(db.Float, nullable=False, default=0.0)
    current_amount = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(40), nullable=False, default="casal")
    target_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="planned")
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
        back_populates="piggy_banks",
    )
    movements = db.relationship(
        "PiggyBankMovement",
        back_populates="piggy_bank",
        cascade="all, delete-orphan",
        lazy=True,
    )

    @property
    def progress_percentage(self):
        """Retorna o percentual de progresso do cofrinho."""
        if self.target_amount <= 0:
            return 100.0 if self.current_amount > 0 else 0.0

        return round(
            min(100.0, max(0.0, (self.current_amount / self.target_amount) * 100)), 2
        )

    @property
    def remaining_amount(self):
        """Retorna o valor restante para atingir a meta."""
        return round(max(0.0, self.target_amount - self.current_amount), 2)

    def __repr__(self):
        return f"<PiggyBank {self.id}>"
