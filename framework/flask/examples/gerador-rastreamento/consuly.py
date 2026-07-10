from run import app
from app.models.tracking_code import TrackingCode

with app.app_context():
    print(TrackingCode.query.count())
    print(TrackingCode.query.all())

    registros = TrackingCode.query.all()

    for registro in registros:
        print(registro.id, registro.codigo, registro.status, registro.criado_em)