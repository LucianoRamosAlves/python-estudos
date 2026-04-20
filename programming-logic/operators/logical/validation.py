
nome = str(input('Digite seu nome: '))

try:
    idade = int(input('Digite sua idade: '))
except ValueError:
    print('idade invalida.')
    print('por favor verifique e tente novamente.')
    idade = False

try:
    saldo = float(input('seu saldo: '))
except ValueError:
    print('saldos digitados incorretamente.')
    print('por favor verifique e tente novamente.')
    saldo = False

#validações
#validação nome
if nome == '':
    print('Opss: preencha campo nome.')

#validação idade
elif idade == False:
    print('Prencha campo idade corretamente.')
elif idade <= 0:
    print('idade invalida.')
elif idade < 18:
    print('Somente maiores de idades.')

#validação saldo
elif saldo == False:
    print('Preencha campo saldo corretamente.')
elif saldo < 0:
    print('Saldo invalido.')
elif saldo == 0:
    print('Sem saldo')
else:
    print('Boas compras')

