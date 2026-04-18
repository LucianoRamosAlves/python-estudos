segredo = 10
numero = -1
contagem = 0

while numero != segredo:

    numero = int(input('Digite seu numero: '))
    print('Boa sorte!')

    if numero == 0:
        print('saindo')
        break

    distancia = abs(numero - segredo)

    if distancia >= 50:
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

# fora do while
if numero == segredo:
    print(f'voce acertou, tentativas {contagem}')
else:
    print('voce desistiu.')