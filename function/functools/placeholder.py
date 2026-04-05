
#? uso quando quero criar uma função que recebe um número variável de argumentos, mas não quero especificar o nome dos argumentos. O placeholder é representado por um asterisco (*) e é usado para indicar que a função pode receber um número indeterminado de argumentos posicionais.

from functools import partial, Placeholder as _

def minha_funcao(a, b, c):
    return a + b + c

# Criando uma função parcial usando o placeholder

soma_com_10 = partial(minha_funcao,_, 10)
# Agora, podemos chamar a função soma_com_10 passando apenas o valor de b e c


resultado = soma_com_10(5, 15)  # Isso é equivalente a chamar minha_funcao(10, 5, 15)

print(resultado)  

def frase(nome, mensagem):
    return f"{nome} diz: {mensagem}"

f = partial(frase, _, "Olá, tudo bem?")
print(f("Alice"))  