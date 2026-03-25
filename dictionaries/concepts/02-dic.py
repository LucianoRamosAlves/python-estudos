pessoa = {
    'nome': 'luciano',
    'idade': 27,
    'cor': 'preto'
}
for i in pessoa:
 print(i, pessoa[i]) #! mas essa não é a melhor opção de ver os valores

for key, value in pessoa.items():
 print(key,value) # essa é mais limpo

 #para adcionar um par chave-valor
pessoa['altura'] = 1.85
print(pessoa)

#? posso adicionar pares novos portanto que a key não seja repitida ou atualizar os valores

#@ para adcionar um novo dicionario ou atualizar
pessoa.update({'idade': 28, 'city': 'codó'})
print(f"${pessoa}")


cor = pessoa.pop('cor', "não achei")
print(f"${cor}")