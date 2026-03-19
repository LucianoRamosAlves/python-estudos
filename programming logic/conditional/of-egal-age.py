print('ACESSO')

print(''' OBSERVAÇÕES: na categoria 
      TERROR somente maiores de 18 anos
      ''')

nome = input('Seu nome:').capitalize()

dataNascimento = int(input('Digite a data de nascimento'))

anoAtual = 2026

idade =  anoAtual - dataNascimento

cartegoria = input(print('Digite sua cartegoria')).lower()



if cartegoria == 'terror':
    if idade < 18:
        print('''olá Senhor(a) {} 
              sua idade é {} anos, 
              sendo menor, não séra possivel'''.format(nome,idade))
    else:
        print(' olá {} , boa seção'.format(nome))
elif idade <= 12:
    print(''' opss, claro {}
          sua idade de {} anos 
          requer um adulto'''.format(nome,idade))
else:
    print(' olá {} , boa seção'.format(nome))

