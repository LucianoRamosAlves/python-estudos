import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from PIL import Image, ImageOps, UnidentifiedImageError


def arquivo_permitido(nome_arquivo):
    if "." not in nome_arquivo:
        return False

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    return extensao in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def gerar_nome_arquivo(nome_arquivo):
    extensao = nome_arquivo.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{extensao}"


def salvar_imagem(
    arquivo,
    pasta,
    largura=400,
    altura=400,
    qualidade=85,
):
    if not arquivo or not arquivo.filename:
        return None

    nome_arquivo = secure_filename(arquivo.filename)

    if not arquivo_permitido(nome_arquivo):
        return None

    limite_tamanho = current_app.config.get("MAX_CONTENT_LENGTH")

    if (
        limite_tamanho
        and arquivo.content_length
        and arquivo.content_length > limite_tamanho
    ):
        return None

    novo_nome = gerar_nome_arquivo(nome_arquivo)

    pasta_upload = os.path.join(
        current_app.config["UPLOAD_ROOT"],
        pasta,
    )

    os.makedirs(pasta_upload, exist_ok=True)

    caminho = os.path.join(
        pasta_upload,
        novo_nome,
    )

    try:
        with Image.open(arquivo) as imagem:
            imagem = ImageOps.exif_transpose(imagem)
            imagem = imagem.convert("RGB")
            imagem.thumbnail((largura, altura))

            imagem.save(
                caminho,
                optimize=True,
                quality=qualidade,
            )

    except (UnidentifiedImageError, OSError):
        return None

    return novo_nome


def salvar_foto_perfil(arquivo):
    return salvar_imagem(
        arquivo,
        pasta="avatars",
        largura=400,
        altura=400,
        qualidade=85,
    )


def remover_imagem(nome_arquivo, pasta):
    if not nome_arquivo:
        return

    caminho = os.path.join(
        current_app.config["UPLOAD_ROOT"],
        pasta,
        nome_arquivo,
    )

    if os.path.isfile(caminho):
        os.remove(caminho)


def remover_foto_perfil(nome_arquivo):
    remover_imagem(
        nome_arquivo,
        "avatars",
    )



