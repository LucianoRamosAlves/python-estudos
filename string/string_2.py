frase = ('Praticando Curso de String')

#// lembrar que começa do indice 0
print(frase[2])
print(frase[0:4])
print(frase[11:26])

print(frase[9:17:2])#@ comeca NO 9 vai até o 17 pulando de 2 em 2

print(frase[:5])
print(frase[16:])

print(frase[9::3])#? começa no 9 e vai até o final, mas como tem o :3, vai pulando de 3 e 3

print(len(frase))

print(frase.count('a'))
print(frase.find('ando')) # mostra a posição que começou

print(frase.find('ang')) # não existe == -1

'Curso' in frase

frase.replace('String', 'Sowftare')

print('-'.join(frase))