episodios = iter(['Episódio 1', 'Episódio 2', 'Episódio 3'])
print(next(episodios))  # Saída: 'Episódio 1'
print(next(episodios))  # Saída: 'Episódio 2'
print(next(episodios))  # Saída: 'Episódio 3'
print(next (episodios, 'fim'))  # Saída: 'fim', pois não há mais itens para iterar  
# Se tentarmos chamar next() novamente, teremos um erro StopIteration, pois não há mais itens para iterar.







# Podemos tratar esse erro usando um bloco try-except:
try:
    print(next(episodios))
except StopIteration:
    print("Não há mais episódios.")