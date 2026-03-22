numeros = [1, 2, 3, 4, 5]
print(max(numeros))
print(min(numeros))
print(sum(numeros))
print(len(numeros))

print("-"*50)

print(all(numeros)) # retorna true pq tem um valor real para cada intem ou seja sem  vakor vazio ou zero ou none
n = [1 , 2 , 0]
l = ['a', 'b' , '']
print(all(n))
print(all(l))

print("-"*50)

#agora com ANY tem que ter pelo menos um valor, já retornar True, no caso a cima tinha que todos tinha que ter valor

print(any(numeros)) # retorna true pq tem um valor real para cada intem ou seja sem  vakor vazio ou zero
n = [1 , 2 , 0]
l = ['a', 'b' , '']
nu = [0 , 0 , 0] #todos os numeroas sem valor
print(any(n))
print(any(l))
print(any(nu))

print("-"*50)

print(numeros.index(4))
print("-"*50)
print(8 in numeros)# false,
print(8 not in numeros)# true,

