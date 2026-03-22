
#| o 1º numero é a linha da matrix
#| o 2º numero é a coluna da matrix

#* só o nome da matrix eu acesso a matrix inteira
#* só um numero eu acesso a linha
#* os 2 numero, linha e coluna, immagine uma sala de cinema

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]

print(matrix)
print(matrix[-1]) #ultima linha
print(matrix[0][1])

#@ fateamento

print(matrix[1][1:])