nome = input("digite seu nome")

separa = nome.split() # separo em espços
print(f"sem primeiro nome é {format(separa[0])} e tem {len(separa[0])} letras")