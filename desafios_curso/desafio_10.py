dias = int(input('quantoas dias'))
km = float(input('quantos km'))


custo = (dias * 60) + (km * 0.15)

print(' voçe passou {} dias e percorreu {} km com o carro'.format(dias, km))
print('*'*50)
print(f'total a pagar será de R$:{custo} reais')