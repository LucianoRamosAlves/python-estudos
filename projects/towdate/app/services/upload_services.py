import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image

def arquivo_permitido(nome_arquivo):
    extensao_permitida = {"png", "jpg", "jpeg"}
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in extensao_permitida

def salvar_foto_perfil(arquivo):
    if arquivo is None:
        return None

    if arquivo.filename == "":
        return None

    nome_arquivo = secure_filename(arquivo.filename)

    if not arquivo_permitido(nome_arquivo):
        return None

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    novo_nome = f"{uuid.uuid4().hex}.{extensao}"

    pasta_upload = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(pasta_upload, exist_ok=True)

    caminho_completo = os.path.join(
    pasta_upload,
    novo_nome
    )

    imagem = Image.open(arquivo)

    imagem.thumbnail((400, 400))

    imagem.save(caminho_completo, optimize=True, quality=85)

    return novo_nome


def remover_foto_perfil(nome_arquivo):
    if not nome_arquivo:
        return

    caminho = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        nome_arquivo
    )

    if os.path.exists(caminho):
        os.remove(caminho)