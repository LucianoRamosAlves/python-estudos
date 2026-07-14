from datetime import datetime

from app.extensions import db


class TrackingCode(db.Model):
    __tablename__ = "tracking_codes"

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(100), unique=True, nullable=False)

    status = db.Column(db.String(30), nullable=False, default="Criado")

    estado = db.Column(db.String(30), nullable=False, default="Ativado")

    categoria_produto = db.Column(db.String(30), nullable=False)

    tipo_entrega = db.Column(db.String(30), nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)