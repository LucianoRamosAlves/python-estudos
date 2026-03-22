

#? o else só faz sentido se usado com o break
#digamos que eu só quero impares, posso verificar antes

numeros = [1, 3, 5, 7]

for numero in numeros:
    if numero % 2 == 0:
        print("numero par achado")
        break
else:
    print("tudo impa")

#** agora, eu quero verificar a qualidade dos dados, quero ver se tem ,, nome null

cores = ['preto', 'verde', 'lilas', 3, 'prata']

for cor in cores:
    if cor == None or cor == "":
        print("Null ou string vazia achado")
        break

    if isinstance(cor, int):
        print("numero achado")
        break
else:
    print("tudo ok")

#@ agora eu quero saber se tem um arquivi suspeito, se tiver eu paro a leitura e mostro

arquivos = ['cor.txt', 'vix.txt', 'insert intal;']

for arquivo in arquivos:
    if arquivo[-1] == ";":
        print("arquivo suspeito achado")
        print(arquivo)
        break
else:
    print("tudo certo")
