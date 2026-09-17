from pathlib import Path
import shutil


# =========================
# PASTA DE TESTE
# =========================

pasta = Path(__file__).parent / "teste_downloads"


# =========================
# CATEGORIAS
# =========================

categorias = {

    "Imagens": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif"
    ],

    "Documentos": [
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".xls",
        ".xlsx"
    ],

    "Videos": [
        ".mp4",
        ".mkv",
        ".avi"
    ],

    "Compactados": [
        ".zip",
        ".rar",
        ".7z"
    ],

    "Programas": [
        ".exe",
        ".msi"
    ],
}


# =========================
# PERCORRER ARQUIVOS
# =========================

for arquivo in pasta.iterdir():

    if not arquivo.is_file():
        continue

    extensao = arquivo.suffix.lower()

    # =========================
    # DESCOBRIR CATEGORIA
    # =========================

    for categoria, extensoes in categorias.items():

        if extensao in extensoes:

            destino = pasta / categoria

            # Cria a pasta caso não exista
            destino.mkdir(
                exist_ok=True
            )

            # Move o arquivo
            shutil.move(
                str(arquivo),
                str(destino / arquivo.name)
            )

            print(
                f"{arquivo.name} → {categoria}"
            )

            break


print()
print("Organização concluída!")