number = float(input('digite um numero : '))
text = ''
tipo = ''


if number % 2 == 0:
    tipo = 'par'
else:
    tipo = 'impar'

if number > 0:
    text = 'Maior que zero'
elif number < 0:
    text = 'Menor que zero'
else:
    text = 'igual a zero'

print(f'Seu numero: {number}\n é {tipo} e {text}')