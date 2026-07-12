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
        registro = None
        pesquisa_realizada = False
        mensagem = None
        tamanho_minimo_codigo = 15  # Defina o tamanho mínimo do código

        if request.method == "POST":
            codigo = request.form.get("codigo").strip() # Remove espaços em branco extras
            pesquisa_realizada = True

            if not codigo:
                mensagem = "Por favor, insira um código para consulta."

            elif len(codigo) < tamanho_minimo_codigo:
                mensagem = f"O código deve ter pelo menos {tamanho_minimo_codigo} caracteres."
                
            else:
                registro = TrackingCode.query.filter_by(codigo=codigo).first()

                if not registro:
                    mensagem = "Código não registrado."

        return render_template("consultas.html", codigo=codigo, registro=registro, pesquisa_realizada=pesquisa_realizada, mensagem=mensagem)