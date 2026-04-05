for i in range(0,6):
    print('oi')
print('fim')

print('=*'*50)

#| a logica é, ele pega o - i- e coloca 1, como não chegou em 6, ele repete oi

for n in range(5 , 0, -1):
    print(n)
    #* aqui, estou mostrando a contagem

print('=*'*50)

    #? agora veja que eu posso trabalhar com inputs, tanto no i ou n , como na função 

numero = int(input('digite um numero'))
for  num in range(0 , numero + 1): # para chegar no numero certo
    print(num)
