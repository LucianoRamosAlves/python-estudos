# lista onde vamos guardar apenas os números válidos
numeros = []

# contador de entradas inválidas (opcional, mas útil)
quantidade_errada = 0


# loop infinito → o programa roda até o usuário digitar "sair"
while True:

    # pede um valor ao usuário (sempre vem como STRING)
    valor = input('Digite um valor: ')

    # verifica se o usuário quer sair
    if valor == 'sair':
        break # sai do loop


    # tenta converter o valor para número (float)
    try:
        numero = float(valor)

    # se der erro (ex: "abc"), entra aqui
    except:
        print('Entrada inválida')
        quantidade_errada += 1 # soma erro
        continue # volta pro início do loop


    # verifica se é número decimal (ex: 2.5)
    if not numero.is_integer():
        print('Apenas inteiros são permitidos')
        quantidade_errada += 1
        continue # ignora e pede outro número


    # agora sabemos que é inteiro → converte de float para int
    numero = int(numero)

    # adiciona o número válido na lista
    numeros.append(numero)


    # agora vem a lógica de classificação

    # número par e positivo
    if numero % 2 == 0 and numero > 0:
        print('Par e positivo')

    # número par e negativo
    elif numero % 2 == 0 and numero < 0:
        print('Par e negativo')

    # número ímpar e positivo
    elif numero > 0:
        print('Ímpar e positivo')

    # número ímpar e negativo
    elif numero < 0:
        print('Ímpar e negativo')

    # caso seja zero
    else:
        print('Zero')


# 🔥 saiu do loop → começa o resumo final

print('\nResumo:')

# verifica se existe pelo menos um número válido
if numeros:

    # quantidade de números válidos
    print('Quantidade:', len(numeros))

    # maior número da lista
    print('Maior:', max(numeros))

    # menor número da lista
    print('Menor:', min(numeros))

# caso nenhum número válido tenha sido digitado
else:
    print('Nenhum número válido foi digitado')
