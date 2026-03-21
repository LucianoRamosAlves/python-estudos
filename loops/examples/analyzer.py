
soma_idade = 0
contador = 0
cont_m = 0

for i in range(1, 3):
    print(f"----- {i}º Pessoa -----")
    nome = str(input("digite seu nome:"))
    idade = int(input("digite a sua idade:"))
    sexo = str(input("SEXO [M/F]"))

    soma_idade += idade
    contador += 1
    media_idade = soma_idade / contador


    if sexo == "s" and idade < 20:
        cont_m += 1

    print(f"nome: {nome}")
    print(f"idade: {idade}")
    print(f"Sexo: {sexo}")

print(f"a media de idade do grupo é de {media_idade} anos")
print(f" total de mulheres menos de 20 anos: {cont_m}")