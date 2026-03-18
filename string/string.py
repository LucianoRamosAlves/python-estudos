senha = "1234"
print(len(senha)) # len() ver o tamanho 
#!posso fazer um verificador de senhas, quantidades 

print("-"*40)

text = '''
 olá, meu nome é Jack, tenho 2 casas, uma azul  e outra amarela, minha casas são antiga, casas do tempo, casas sem nexo casas casas iihlehgjerghejkrferg casas jbejglebgletjgtj casas '''
print(text.count('casas')) # aqui ver a quantidade de palavra repetida
#! aqui eu posso fazer um input aonde tem um texto e depois outro input para pesquisar quantas palavras

print("-"*40)


# aqui eu troco caracteres
preco = '22,50'
print(preco.replace(",", "."))
telefone = '55-99-988213473'
print(telefone.replace("-", "/")) 
#** poderia ser "-", "" nesse caso 5599988213473

print("-"*40)
nome =  "Prin"
idade = 27
estado = "maranhão"
print(f"meu nome é {nome} e tenho {idade} anos sou do {estado}")

print("-"*40)

#? aqui ele cria listas com os grupos 
data = "09/02/2026"
print(data.split("/"))

data_file =  "1234,max,USA, 1999-03-25,M,+*"
print(data_file.split("/"))

print("-"*40)

frase = "Princesa"
print(frase[0])
print(frase[-3]) # essa contagem aqui é de tras para frente
print(frase[0:4]) # vai do indice 0 até o 4 mas lembre-se que é um antes do 4, ouseja para no indice 3
print(frase[:4])
print(frase[5:])

print("-"*40)

texto = "   #bom dia   ".strip()
print(texto)
print(texto.lstrip()) # remove espaco em branco a esquerda
print(texto.rstrip()) # remove espaco na direita
print(texto.strip()) # remove todos espacos em branco direita e esquerda
 #!-------------------não funcionou-----------------------------------
#@ agora tem como remover tudo, que quiser mas tem que falar o que com strip()
print(texto.strip("#"))


print("-"*40)


phone = '99-9883264'
print(phone.startswith('99')) #* procura se 99 ta

email = 'lucas@gmail'
print("@" in email) #// se @ ta no email