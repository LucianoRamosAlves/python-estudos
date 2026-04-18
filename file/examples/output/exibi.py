with open("nomes.txt", "r") as arquivo:
    arquivo.seek(3) # move o cursor para a posição 3 (após "nom") para sobrescrever "nome" por "idade"

    print(arquivo.read()) # lê o conteúdo do arquivo a partir da posição atual do cursor (posição 3) e imprime na tela
    print(arquivo.tell()) # mostra a posição atual do cursor (deve ser 3)

    print(arquivo.seek(10, 0)) # move o cursor para a posição 10 (após "ana: 25\n") para sobrescrever "ana" por "diego"
    print(arquivo.read()) # lê o conteúdo do arquivo a partir da posição atual do cursor