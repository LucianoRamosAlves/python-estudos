letras = [ 'a', 'b ', 'c']
numeros = ['1', '2', '3']
print(letras)
print(type(letras))

print("-"*30)
mix = ['1', 'True']
print("-"*30)

palavra = list('frase') #@ uso list() e crio uma lista
print(palavra)
print("-"*30)
#* posso usar um range
n = list(range(0,5))
print(n)
print("-"*30)
# lista dentro da lista
matrix = [['a', 'b'],
          ['1', '2', '3'],
          [True]]
print(matrix)
print("-"*30)
print(matrix[1]) #imprime a linha da matrix
print(matrix[1][1]) #peguei  o indice 1
