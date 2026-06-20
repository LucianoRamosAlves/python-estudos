import operator

#* uso quando quero realizar operações matemáticas ou lógicas de forma mais concisa e legível. O módulo operator fornece funções que correspondem a operadores matemáticos e lógicos, permitindo que você escreva código mais claro e expressivo.


print(operator.add(2, 3)) #soma
print(operator.mul(4, 5))  #multiplicação
print(operator.sub(10, 7)) #subtração
print(operator.truediv(10, 2)) #divisão
print(operator.pow(2, 3)) #potência
print(operator.mod(10, 3)) #módulo
print(operator.neg(5)) #negativo
print(operator.eq(5, 5)) #igualdade
print(operator.gt(10, 5)) #maior que
print(operator.itemgetter(1)([10, 20, 30])) #pegar item
print(operator.attrgetter('real')(3 + 4j)) #pegar atributo
print(operator.methodcaller('upper')('hello')) #chamar método
print(operator.contains([1, 2, 3], 2)) #verificar se contém
print(operator.countOf([1, 2, 3, 2, 1], 2)) #contar ocorrências
print(operator.is_(5, 5)) #identidade
print(operator.is_not(5, 5)) #não identidade
print(operator.truth(0)) #verificar verdade
print(operator.floordiv(10, 3)) #divisão inteira
print(operator.lshift(1, 2)) #deslocamento à esquerda
print(operator.rshift(8, 2)) #deslocamento à direita
print(operator.xor(5, 3)) #xor bit a bit
print(operator.invert(5)) #inversão bit a bit
print(operator.and_(5, 3)) #and bit a bit
print(operator.or_(5, 3)) #or bit a bit
print(operator.index(5)) #converter para inteiro
print(operator.length_hint([1, 2, 3])) #dica de comprimento
print(operator.setitem([1, 2, 3], 1, 10)) #definir item
print(operator.delitem([1, 2, 3], 1)) #deletar item
print(operator.getitem([1, 2, 3], 1)) #pegar item
print(operator.attrgetter('imag')(3 + 4j)) #pegar atributo


