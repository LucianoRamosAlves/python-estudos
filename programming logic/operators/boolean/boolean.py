print(bool(123)) # verifica se tem algun valor
print(bool("olá")) # verifica se tem algun valor

print(bool()) # esse ta vazio

#? 0 ou "" ou Nome são considerados vazios e retorna false

nome = ""
idade = 27
tel = 0

#** tenho 2 metodos 
# **[1] verifico se pelo menos 1 variavel foi preenchia, TRUE-any()
print(any([nome, idade, tel]))

#** [2] só retorna True  se todas forem preenchidas-all()
print(all([nome, idade, tel]))