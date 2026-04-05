
#| para eu evitar o uso exessivo de condicionais if-elif-else para lidar com diferentes tipos de dados ou casos específicos. O singledispatch é um decorador que permite criar funções genéricas que podem ser especializadas para diferentes tipos de argumentos, sem a necessidade de escrever código condicional complexo.

from functools import singledispatch

@singledispatch
def responder(x):
    return f"Não sei como responder a {x}"

@responder.register
def _(x: int):
    return f"Você me deu um número inteiro: {x}"

@responder.register
def _(x: str):
    return f"Você me deu uma string: {x}"

print(responder("oi"))

@responder.register
def _(arg: list):
    return f"Você me deu uma lista: {arg}"

print(responder((1, 2, 3)))

@singledispatch
def fun(arg):
    print(f"Tipo de argumento não suportado: {type(arg)}")
    
    
@fun.register
def _(arg: list):
    print(f"Você me deu uma lista: {arg}")
    for i, item in enumerate(arg):
        print(f"Índice {i}: {item}")
        
print(fun([9, 8, 7]))

# O singledispatch é uma ferramenta poderosa para criar funções genéricas que podem ser especializadas para diferentes tipos de argumentos, tornando o código mais limpo e fácil de manter. Ele é especialmente útil quando você tem uma função que precisa lidar com diferentes tipos de dados ou casos específicos, sem a necessidade de escrever código condicional complexo.

# TODO WIP: falta terminar o exemplo do singledispatch, e adicionar mais exemplos de uso.