from operator import itemgetter

#* itemgetter é uma função que retorna um objeto chamável (callable) que pode ser usado para acessar um item específico de um objeto, como uma lista, tupla ou dicionário. Ele é útil para extrair valores de estruturas de dados de forma concisa e eficiente.

#| exemplo de uso do itemgetter para acessar o segundo elemento de uma lista

lista = [ "maçã", "banana", "laranja"]
segundo_elemento = itemgetter(1)
print(segundo_elemento(lista))  

