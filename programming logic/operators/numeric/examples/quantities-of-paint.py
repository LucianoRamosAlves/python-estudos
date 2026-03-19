import math

nome = input('digite seu nome').capitalize()
a = float(input('digite uma altura'))
l = float(input('digite uma largura'))

area = a * l
qtdTintas = math.ceil(area / 2)
valorTinta = 18.75
gastos = qtdTintas * valorTinta

print(f''' olá {nome}, sua parede tem  uma dimensão de {a}x{l} portanto uma area de :
      {area:.2f} metros ao quadrado e 
      são pecisos {qtdTintas} latas de tintas
      cada tinta custa R$ {valorTinta} reias
      total  = R$ {gastos:.2f} reais ''')
#! posso fazee um if, se for sobrar tinta ,se a divisao conter sobras, posso aletar que vai sobrar tints 
#? em um desafio mais hard, posso até dizer o quanto de tinta sobra