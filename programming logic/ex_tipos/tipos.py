a = input('digite algo')
print('O valor digitado foi {:-^10} \n veja as caracteristica dele ' \
'abaixo'.format(a))



print('o tipo desse valor é ', type(a))
print('só tem espaços ? ', a.isspace())
print('é um numero  ?', a.isnumeric())
print('é um alfabético ?', a.isalpha())
print('é um alfanumérico ?', a.isalnum())
print('ésta em maiuscula ?', a.isupper())
print('esta em minuscula ?', a.islower())
print('esta capitalizada ?', a.istitle())