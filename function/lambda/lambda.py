multiple = lambda x: x * 2
print(multiple(2)) # eu meio que passo o valor de x

add = lambda x,y : x + y
print(add(1,2))

check = lambda i: i in "python"
print(check('u')) #pecorro e vejo de está na palavra



#| paaso a passo, quero tranformar essa lista em float

precos = ['R$90.8', 'R$10.8', 'R$90.00',]
#lambda precos: float(p.replace('R$', '')) # 1 aplico a formula achada
# map(lambda precos: float(p.replace('R$', '')), precos) # aplico a lista usando map
# list(map(lambda precos: float(p.replace('R$', '')), precos)) # uso o list
print(list(map(lambda precos: float(precos.replace('R$', '')), precos)))

#| primeiro, voce tenta tranformar um intem só, para pegar a logica

p = "R$90.8"
# tiro o caractere
p.replace('R$', '')
#depois coloquei em float
#! só pega em print, faz assim só para ver

print(float(p.replace('R$', '')))

#| agora tenho a formula, só colocar em lambda

