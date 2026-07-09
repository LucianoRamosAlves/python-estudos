from flask import render_template, request
from services.gerador_codigo import gerar_codigo

def register_routes(app):

    @app.route("/", methods=["GET", "POST"])
    def index():
        codigo = None
        mensagem = None
        
        if request.method == "POST":
            codigo = gerar_codigo()
            mensagem = "Código gerado com sucesso!"

        return render_template("index.html", codigo=codigo, mensagem=mensagem)