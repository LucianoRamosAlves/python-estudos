def validação_quantidades_pessoas():
    if quantidade_pessoas == 0:
        print('Não há passageiros')
    elif quantidade_pessoas < 0:
        print('Quantidade de pessoas invalida')
    elif quantidade_pessoas > 1000:
        print('Quantidade de pessoas além do limite')

    return quantidade_pessoas

def validação_quantidades_carros():
    if quantidade_carros == 0:
        print('Não há carros disponiveis')
    elif quantidade_carros < 0:
        print('Quantidade de carros invalido')
    elif quantidade_carros > 200:
        print('Quantidade de carros além do limite')

    return quantidade_carros

def calculos():
    quantidade_vagas = quantidade_carros * 4
    if quantidade_pessoas > quantidade_vagas:
        carros_cheios = quantidade_pessoas // 4
        pessoas_esperando = quantidade_pessoas % 4
        pessoas_carro = quantidade_carros * 4
        pessoas_emPe = quantidade_pessoas - pessoas_carro
        print('Infelizmente não terá vagas para todos')
        print(f' No momento {quantidade_carros} carros levara {pessoas_carro} pessoas e ficara {pessoas_emPe} pessoas ')
        print(f'Serão nescessarios {carros_cheios} carros e {pessoas_esperando} ficaram esperando')


try:
    quantidade_pessoas = int(input('Digite o total de pessoas'))
    validação_quantidades_pessoas()

    quantidade_carros = int(input('carros disponvéis ?'))
    validação_quantidades_carros()

    calculos()
  

except:
    print('Valor de Pessoas ou carros invalidos')



    
