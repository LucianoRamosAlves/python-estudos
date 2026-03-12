nome = input('digite algo e verefique')

a = nome.isspace()
b = nome.isnumeric()
c = nome.isalpha()
d = nome.isalnum()
e = nome.isupper()
f = nome.islower()
g = nome.istitle()
h = type(nome)

print(h)
print(''' olá os dados digitados são:
      
      
      é do tipo-----{}
      só tem espaços-----{}
      é um numero-----{}
      é um alfabetico-----{}
      tem letra ou numero-----{}
      está em maiuscula-----{}
      está em minuscula-----{}
      esstá capitalizada------{}
      '''.format(h, a, b, c, d, e, f, g))
