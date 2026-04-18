idades = {
    "ana": 25,
    "bruno": 30,
    "carla": 22,
    "diego": 28,
    "elena": 26
}

# salva o dicionário em um arquivo texto usando o formato "nome idade" em cada linha
with open("nomes.txt", "r") as arquivo:
    for nome in idades:
        arquivo.write(f"nome: {idades[nome]}\n")

arquivo.seek(3) # move o cursor para a posição 3 (após "nom") para sobrescrever "nome" por "idade"

print(arquivo.read()) # lê o conteúdo do arquivo a partir da posição atual do cursor (posição 3) e imprime na tela
print(arquivo.tell()) # mostra a posição atual do cursor (deve ser 3)