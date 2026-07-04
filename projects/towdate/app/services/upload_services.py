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


def gerar_nome_arquivo(extensao):
    return f"{uuid.uuid4().hex}.{extensao}"


def obter_tamanho_arquivo(arquivo):
    if getattr(arquivo, "content_length", None):
        return arquivo.content_length

    stream = getattr(arquivo, "stream", None)
    if stream is None:
        return None

    posicao_atual = stream.tell()
    stream.seek(0, os.SEEK_END)
    tamanho = stream.tell()
    stream.seek(posicao_atual)
    return tamanho


def extensao_por_formato_imagem(formato):
    mapa = {
        "JPEG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "GIF": "gif",
    }
    return mapa.get(formato or "")


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
    tamanho_arquivo = obter_tamanho_arquivo(arquivo)

    if limite_tamanho and tamanho_arquivo and tamanho_arquivo > limite_tamanho:
        return None

    pasta_upload = os.path.join(
        current_app.config["UPLOAD_ROOT"],
        pasta,
    )

    os.makedirs(pasta_upload, exist_ok=True)

    try:
        with Image.open(arquivo) as imagem:
            formato = (imagem.format or "").upper()
            extensao_real = extensao_por_formato_imagem(formato)

            if not extensao_real:
                return None

            if extensao_real not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                return None

            if imagem.width * imagem.height > 40_000_000:
                return None

            novo_nome = gerar_nome_arquivo(extensao_real)
            caminho = os.path.join(pasta_upload, novo_nome)

            imagem = ImageOps.exif_transpose(imagem)

            if extensao_real in {"png", "webp"}:
                if imagem.mode not in {"RGB", "RGBA"}:
                    imagem = imagem.convert("RGBA")
            else:
                imagem = imagem.convert("RGB")

            imagem.thumbnail((largura, altura))

            parametros_salvamento = {
                "optimize": True,
            }

            if extensao_real in {"jpg", "jpeg", "webp"}:
                parametros_salvamento["quality"] = qualidade

            imagem.save(caminho, **parametros_salvamento)

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


def salvar_foto_casal(arquivo):
    return salvar_imagem(
        arquivo,
        pasta="couples",
        largura=900,
        altura=900,
        qualidade=88,
    )


def remover_foto_casal(nome_arquivo):
    if nome_arquivo in {"default.jpg", "couples/default.jpg"}:
        return

    remover_imagem(
        nome_arquivo,
        "couples",
    )
