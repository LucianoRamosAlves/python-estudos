from flask import render_template, request
from app.services.gerador_codigo import gerar_codigo
from app.models.tracking_code import TrackingCode
from app.extensions import db

def register_routes(app):

    @app.route("/", methods=["GET", "POST"])
    def index():
        codigo = None
        mensagem = None
        
        if request.method == "POST":
            codigo = gerar_codigo()

            novo_codigo = TrackingCode(
                codigo=codigo)
            
            db.session.add(novo_codigo)
            db.session.commit()

            mensagem = "Código gerado com sucesso!"

        return render_template("index.html", codigo=codigo, mensagem=mensagem)

    @app.route("/consultas", methods=["GET", "POST"])
    def consultas():
        codigo = None
        mensagem = None

        if request.method == "POST":
            codigo = request.form.get("codigo")
 
            registro = TrackingCode.query.filter_by(codigo=codigo).first()

            if registro:
                mensagem = f"Status: {registro.status} \n Criado em: {registro.criado_em}"
            else:
                mensagem = "Código não encontrado."

        return render_template("consultas.html", codigo=codigo, mensagem=mensagem)