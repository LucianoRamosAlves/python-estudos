frutaria = [
    ("banana", 2),
    ("maçã", 3),
    ("laranja", 1),
    ("uva", 4),
    ("abacaxi", 5)
]

from operator import itemgetter

quantidades = itemgetter(1)
print(list(map(quantidades, frutaria))) #pegar as quantidades usando itemgetter

ordenado_por_quantidade = sorted(frutaria, key=quantidades)
print(ordenado_por_quantidade)