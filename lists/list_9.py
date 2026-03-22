letras = [ 'a', 'b', None, 'c'  , False,'4'] 
print(list(filter(bool, letras)))
# ou ao invés do None posso usar o bool

#@ perceba que ficou o 4 na lista
letras_n = ['a', 'b', 'c', '4']
print(list(filter(str.isalpha, letras_n)))
for l in filter(str.isalpha, letras_n):
    print(l)