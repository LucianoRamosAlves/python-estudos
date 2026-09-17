from pathlib import Path


nome_procurado = input("Digite o nome do arquivo: ").lower()

pasta_usuario = Path.home()

print("Procurando...")


for arquivo in pasta_usuario.rglob("*"):

    if arquivo.is_file():

        if nome_procurado in arquivo.name.lower():

            print()
            print("Arquivo encontrado!")
            print(arquivo)

            break