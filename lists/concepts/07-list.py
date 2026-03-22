letras = ['c', 'b', 'd', 'a']
numeros = [ 1 , 2 , 3]
letras_Copia = letras.copy()
#! eu uso a copia, qualquer erro eu tenho o original

letras_Copia.append('e')
letras_Copia.sort()
print(letras_Copia)
print(letras)




#| aqui eu estico a variavel e coloco, junto com outra
numeros.extend(letras)# pega o numero e estendi as letras
print(numeros)


#| aqui eu emparelho os intens, combino de forma organizado
combo = list(zip(letras , numeros))
print(combo)

ids = [101, 307, 587]
nome = ['alex', 'pedro', 'teu']

print(list(zip(ids,nome)))


