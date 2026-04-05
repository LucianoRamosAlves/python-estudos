pessoas = [
    {'nome': 'Alice', 'idade': 30, 'altura': 1.65},
    {'nome': 'Bob', 'idade': 25, 'altura': 1.75},
    {'nome': 'Charlie', 'idade': 35, 'altura': 1.80}
]

mais_velho = max(pessoas, key=lambda p: p['idade'])
print(f'O mais velho é {mais_velho["nome"]} com {mais_velho["idade"]} anos.')

mais_baixo = min(pessoas, key=lambda p: p['altura'])
print(f'O mais baixo é {mais_baixo["nome"]} com {mais_baixo["altura"]} metros.')

#key() 