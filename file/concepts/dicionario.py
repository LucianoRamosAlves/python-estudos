print('oi')

with open("dicionario.txt", "r") as f:
    for linha in f:
        print(linha.strip())