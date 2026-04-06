from operator import itemgetter

dados = [
    ("João", 25, "Engenheiro"),
    ("Maria", 30, "Médica"),
    ("Pedro", 22, "Estudante"),
    ("Ana", 28, "Advogada")
]

#| usando itemgetter para ordenar a lista de dados pelo idade (índice 1)

ordenado_por_idade = sorted(dados, key=itemgetter(1))
print(ordenado_por_idade)

nome = itemgetter(0)
print(nome(dados[0])) 