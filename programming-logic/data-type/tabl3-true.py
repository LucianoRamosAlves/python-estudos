A = int(input('digite o numero A: '))

B = int(input('digite o numero B: '))

print(f'tabela da verdade entre os numeros A: {A} e B: {B}')

if A > B:
    print(f'{A} é maior {B}')
elif B > A:
    print(f'{B} é maior {A}')
else:
    print(f'{A} é igual {B}')

if A > 0:
    print(f'{A} positivo')
else:
    print(f'{A} negativo')


if B > 0:
    print(f'{B} positivo')
else:
    print(f'{B} negativo')