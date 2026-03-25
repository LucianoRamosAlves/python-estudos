# quando não sei os valores, crio o dicionario e coloco em todos nome
pessoa = dict.fromkeys(["nome", "idadade", "city"], None)
print(f"${pessoa}")

# depois eu faço
pessoa["city"] = 'codo'
print(f"${pessoa}")