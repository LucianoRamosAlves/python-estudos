import math

preco = 78.56145
print(5 // 2) # pego a parte inteira sem o resto
print( 5 % 2) # pego só o resto da divisão

print(round(preco)) # arredonda, nativo
print(round(preco,2))# pega até a casa decimal 2
print(math.ceil(preco)) # arredonda para cima
print(math.floor(preco)) # arredonda para baixo

print(preco.is_integer()) # verifica se o numero é inteiro

#@ agora essa outra eu verifico o tipo que eu quiser

print(isinstance(preco, float))
