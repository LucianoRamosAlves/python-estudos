
sexo = ""

print("digite seu sexo")
while sexo != "m" and sexo != "f":
    sexo = str(input("Digite seu sexo [M] / [F]")).lower()
    if sexo == "m":
        print("masculino")
    elif sexo == "f":
        print("feminino")
    else:
        print("tente novamente")
