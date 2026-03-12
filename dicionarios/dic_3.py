# quando não sei os valores

pessoa = dict.fromkeys(["nome", "idadade", "city"], None)
print(f"${pessoa}")

# depois eu faço
pessoa["city"] = 'codo'
print(f"${pessoa}")