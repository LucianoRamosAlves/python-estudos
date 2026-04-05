nota_a = [ 40, 50, 30, 20, 10]
nota_b = [ 70, 50]

#| uso lamda para criar funções anônimas, ou seja, funções sem nome. Elas são úteis para operações simples e de uso único, como em funções de ordem superior (map, filter, reduce) ou para criar funções rápidas e concisas.

lambda_a = lambda x: x + 1
print(list(map(lambda_a, nota_a)))


lambda_soma = lambda x, y: x + y
print(list(map(lambda_soma, nota_a, nota_b)))

lambda_soma_a = lambda x: x + x
print(list(map(lambda_soma_a, nota_a)))

#@ devo usar o lambda somente quando for uma função simples, caso contrário, é melhor usar uma função tradicional com def. O lambda é útil para funções pequenas e de uso único, enquanto o def é mais adequado para funções mais complexas ou que serão reutilizadas.

#! exemplo mais profissional usando

def media(x):
    return sum(x) / len(x)

print(media(nota_a))

# poderia ser feito com lambda, mas não é recomendado para funções mais complexas: e lambda_media = lambda x: sum(x) / len(x), mas 
