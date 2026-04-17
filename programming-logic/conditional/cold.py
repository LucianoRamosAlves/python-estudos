segredo = 10
numero = -1
contagem = 0

while numero != segredo:

    numero = int(input('Digite seu numero: '))
    print('Boa sorte!')

    # Calcula distância do segredo
    distancia = abs(numero - segredo)

    # Define status corretamente
    if distancia >= 50
        status = 'frio'
    elif distancia >= 20:
        status = 'morno'
    elif distancia >= 10:
        status = 'quente'
    else:
        status = 'muito quente'

    if numero < segredo:
        print('opss: o numero é maior')
        print(f'seu status da rodada: {status}')
    
    elif numero > segredo:
        print('opss: o numero é menor')
        print(f'seu status da rodada: {status}')

    contagem += 1

print(f'voce acertou, tentativas {contagem}')