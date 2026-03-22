letras = [ 'a', 'b', 'c'] #lista original
numeros = ['1', '2', '3']

nova_lista = []

for i in letras:
    nova_lista.append(i.upper())# aqui eu estou percorrendo e colocando na nova lista e trasformando
print(nova_lista)




print(list(enumerate(letras, start=1))) # me retorna o indice
 #@ou posso usar assim
for index, value in enumerate(letras):
    print(index, value)

    #? posso fazer isso tambem com zip, pois tenho 2 valores retornados

print("-"*30)








#| usado para parear 2 listas
for l, n in zip(letras , numeros):
    print(l , n)

 #* agora se eu quiser fazer alguma trasformação uso o map



print(list(map(str.upper, letras)))
print(list(map(int, numeros)))

print("-"*30)
#@ eu posso tirar os espaços
nome = ['  maria', 'pedro ', '  marcos  ']
print(nome)
for no in map(str.strip, nome):
    print(no)

# NOTE

print("""--- MENU PRINCINPAL ---
      
      [1] Consultas
      [2] Quantidades
      [3] Status
      [4] Adicionar
      [5] Remover
      [6] Sair

      
      [1] ver grupo mais 20
      [2] ver grupo mais 60
      [3] quantidade no grupo mais 20
      [4] quantidade no grupo mais 60
      [5] mais velho no grupo mais 20
      [6] mais velho no grupo mais 60
      [3] adicionar no grupo mais 20
      [3] adicionar no grupo mais 60
      [4] adicionar geral
      [4] ver grupo grupo mais 20
      [4] ver grupo grupo mais 20
      [7] ver geral 
      [3] remove no grupo mais 20
      [3] remover no grupo mais 60""")
