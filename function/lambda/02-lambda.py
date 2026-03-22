
#| quero só os maiores que 100

precos = [120, 56, 89, 790, 500]

# primeiro eu pego a logica

#p > 100

#lambda p: p > 100 agora que tenho a logica coloco em lambda

# quero filtrar, uso filter, e passo oque a ser filtrado
# filter(lambda p: p > 100, precos)

# usa a  list pra ver os resultados
print(list(filter(lambda p: p > 100, precos)))

