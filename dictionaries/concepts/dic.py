pessoa = {
    'nome': 'luciano',
    'idade': 27,
    'cor': 'preto'
}
print(pessoa)

#para acessar uso a chave
print(pessoa['cor'])

#ele é mutavel
pessoa['idade'] = 28
print(pessoa['idade'])

#para evitar erros, casos eu procuro algo que não exista, serve para procurar é ,melhor esse
print(pessoa.get('carro')) #recebi none ou
print(pessoa.get('carro','valor desconhecido'))
print(pessoa.get('nome'))

#para ver se é menbro do meu dicionario
print('cor' in pessoa)

#retorna todas as chaves
print(pessoa.keys())
#retorna os valores
print(pessoa.values())
#para obter os 2
print(pessoa.items()) ##@ melhor usa esse, esse retorna uma tupla