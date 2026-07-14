from flask import render_template, request
from app.services.gerador_codigo import gerar_codigo
from app.models.tracking_code import TrackingCode
from app.extensions import db

def register_routes(app):

    @app.route("/", methods=["GET", "POST"])
    def index():
        codigo = None
        mensagem = None
        categoria_produto = None
        tipo_entrega = None
        pesquisa_realizada = False
        
        if request.method == "POST":
            pesquisa_realizada = True
            categoria_produto = request.form.get("categoria_produto")
            tipo_entrega = request.form.get("tipo_entrega")

            if not categoria_produto or not tipo_entrega:
                mensagem = "Por favor, selecione uma categoria de produto e um tipo de entrega."
                return render_template("index.html", codigo=codigo, mensagem=mensagem, categoria_produto=categoria_produto, tipo_entrega=tipo_entrega, pesquisa_realizada=pesquisa_realizada)

            
            codigo = gerar_codigo(categoria_produto, tipo_entrega)

            novo_codigo = TrackingCode(
                codigo=codigo,
                categoria_produto=categoria_produto,
                tipo_entrega=tipo_entrega)
            
            db.session.add(novo_codigo)
            db.session.commit()

            mensagem = "Código gerado com sucesso!"

        return render_template("index.html", codigo=codigo, mensagem=mensagem, categoria_produto=categoria_produto, tipo_entrega=tipo_entrega, pesquisa_realizada=pesquisa_realizada)

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

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        codigo = None
        registro = None
        mensagem = None
        if request.method == "POST":
            codigo = request.form.get("codigo").strip()
            registro = TrackingCode.query.filter_by(codigo=codigo).first()
            if not registro:
                mensagem = "Código não registrado."
        return render_template("admin.html", codigo=codigo, registro=registro, mensagem=mensagem)
    
    @app.route("/admin_pesquisas", methods=["GET"])
    def admin_pesquisas():
        codigo = None
        registro = None
        mensagem = None

        if request.method == "GET":
            codigo = request.args.get("codigo").strip() if request.args.get("codigo") else None
            registro = TrackingCode.query.filter_by(codigo=codigo).first() if codigo else None
            if codigo and not registro:
                mensagem = "Código não registrado."

            if registro:
                mensagem = TrackingCode.query.filter_by(codigo=codigo).all()
        





        return render_template("admin_pesquisas.html", codigo=codigo, registro=registro, mensagem=mensagem)