matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]
#adiciona na ultima
matrix.append(['x', 'y', 'z'])

#adiciono uma linha
matrix.insert(1, ['a', 'a', 'a'])

#posso adcionar especificando mais
matrix[1].append('r')

matrix.remove(['a', 'a', 'a'])#removo pelo valor
matrix[1].remove('r')#removo pelo valor

 #! o mesmo para o pop(), mas o  pop é pelo indice