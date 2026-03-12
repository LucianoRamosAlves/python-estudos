frutas = ['banana', 'maça', 'uva', 'abacaxi', 'pessego', 'goiaba', 'pera', 'melancia', 'morango', 'manga']


nova = input('digite uma fruta').lower()
if nova in frutas:
    print('essa fruta já existe')
else:
    frutas.append(nova)
    print('fruta adicionada')





print('a primeira fruta:' + frutas[0])
print('a ultima fruta:' + frutas[-1])

print('quantidade de frutas é' , len(frutas))

print('adicionando na ultima lista :' ,frutas.append('mamão') , frutas
[-1])
#! lista atualizada
print('adicionando no segundo :' ,frutas.insert(1,'caju') , frutas[1])
#! lista atualizada

print('removendo pelo nome:' ,frutas.remove('pera') , frutas[6])
print('removendo pelo indice:' , frutas.pop(4))
#! lista atualizada

ordenados = sorted(frutas)
#print(ordenados)

print(frutas.count('pera'))

print('uva' in frutas)

frutas_M = []

for fruta in frutas:
    if fruta.lower().startswith('m'):
       frutas_M.append(fruta)
print('frutas com M:' ,frutas_M)

for index, value in enumerate(frutas):
    print(index, value)

tamanhos = []

for frut in frutas:
    tamanhos.append(len(frut))
resultado = list(zip(frutas, tamanhos))
print(resultado)



