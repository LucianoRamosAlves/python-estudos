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

            if not categoria_produto:
                mensagem = "Por favor, selecione uma categoria de produto."
                return render_template("index.html", codigo=codigo, mensagem=mensagem, categoria_produto=categoria_produto, pesquisa_realizada=pesquisa_realizada)

            elif not tipo_entrega:
                mensagem = "Por favor, selecione um tipo de entrega."
                return render_template("index.html", codigo=codigo, mensagem=mensagem, tipo_entrega=tipo_entrega, pesquisa_realizada=pesquisa_realizada)

            
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

                elif registro and registro.estado == "cancelado":
                    mensagem = "Este código foi cancelado."
                    registro = None  # Não exibir o registro cancelado

                elif registro and registro.estado == "deletado":
                    mensagem = "Este código não está mais disponível para consulta."
                    registro = None  # Não exibir o registro deletado


        return render_template("consultas.html", codigo=codigo, registro=registro, pesquisa_realizada=pesquisa_realizada, mensagem=mensagem)

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        codigo = None
        registro = None
        mensagem = None
        pesquisa_realizada = False
        descricao_problema = None

        if request.method == "POST":
            pesquisa_realizada = True
            codigo = request.form.get("codigo").strip()
            registro = TrackingCode.query.filter_by(codigo=codigo).first()

            if codigo == "":
                mensagem = "Por favor, insira um código para consulta."

            elif not registro:
                mensagem = "Código não registrado."

            elif registro:
                novo_status = request.form.get("novo_status")
                novo_estado = request.form.get("novo_estado")
                novo_tem_problema = request.form.get("novo_tem_problema")
                b_acao = request.form.get("b_acao")

                if b_acao == "deletar":
                    registro.estado = "deletado"
                    db.session.commit()
                    codigo = None
                    registro = None
                    mensagem = "Código deletado com sucesso."

                else:

                    if novo_status:
                        registro.status = novo_status

                    if novo_estado:
                        registro.estado = novo_estado

                    if novo_tem_problema == "resolvido":  
                        registro.tem_problema = False
                    elif novo_tem_problema == "nao_resolvido":
                        registro.tem_problema = True

                    if novo_status or novo_estado or novo_tem_problema:
                        db.session.commit()
                        mensagem = "Dados atualizados com sucesso."


        return render_template("admin.html", codigo=codigo, registro=registro, mensagem=mensagem, pesquisa_realizada=pesquisa_realizada, descricao_problema=descricao_problema)
    
    @app.route("/admin_pesquisas", methods=["GET"])
    def admin_pesquisas():
        codigos = []
        codigo = None
        registro = None
        mensagem = None
        quantidade_codigos = 0
        pesquisa_quantidade = False

        if request.method == "GET":
            filtro_categoria = request.args.get("filtro_categoria")
            filtro_status = request.args.get("filtro_status")
            filtro_tipo_entrega = request.args.get("filtro_tipo_entrega")
            filtro_problemas = request.args.get("filtro_problemas")
            filtro_acoes = request.args.get("filtro_acoes")
            b_acao = request.args.get("b_acao")

            query = TrackingCode.query

            if filtro_categoria:
                query = query.filter_by(categoria_produto=filtro_categoria)
            
            if filtro_status:
                query = query.filter_by(status=filtro_status)

            if filtro_tipo_entrega:
                query = query.filter_by(tipo_entrega=filtro_tipo_entrega)

            if filtro_acoes:
                query = query.filter_by(estado=filtro_acoes)

            if filtro_problemas:
                if filtro_problemas == "resolvidos":
                    query = query.filter_by(tem_problema=False)
                elif filtro_problemas == "nao_resolvidos":
                    query = query.filter_by(tem_problema=True)

            if b_acao:
                if b_acao == "ver_codigos":
                    codigos = query.all()

                elif b_acao == "quantidade":
                    pesquisa_quantidade = True
                    quantidade_codigos = query.count()

        return render_template("admin_pesquisas.html", codigo=codigo, registro=registro, mensagem=mensagem, codigos=codigos, lista_codigos=filtro_categoria, quantidade_codigos=quantidade_codigos, pesquisa_quantidade=pesquisa_quantidade)

    @app.route("/problemas", methods=["GET", "POST"])
    def problemas():
        codigo = None
        registro = None
        mensagem = None
        pesquisa_realizada = False
        descricao_problema = None   

        if request.method == "POST":
            pesquisa_realizada = True
            codigo = request.form.get("codigo").strip()
            descricao_problema = request.form.get("descricao_problema")
            registro = TrackingCode.query.filter_by(codigo=codigo).first()

            if codigo == "":
                mensagem = "Por favor, insira um código para consulta."

            elif not registro:
                mensagem = "Código não registrado."

            elif registro and registro.estado == "cancelado":
                mensagem = "Este código foi cancelado."
                registro = None  # Não exibir o registro cancelado

            elif registro and registro.estado == "deletado":
                mensagem = "Este código não está mais disponível para consulta."
                registro = None  # Não exibir o registro deletado

            else:
                if registro:
                    registro.tem_problema = True
                    registro.descricao_problema = descricao_problema
                    db.session.commit()
                    mensagem = "Problema registrado com sucesso."

        return render_template("problemas.html", codigo=codigo, registro=registro, mensagem=mensagem, pesquisa_realizada=pesquisa_realizada)