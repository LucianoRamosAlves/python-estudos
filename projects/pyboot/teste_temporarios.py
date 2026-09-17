import tempfile
from pathlib import Path


# Descobre a pasta de temporários do Windows
pasta_temp = Path(tempfile.gettempdir())


print("Pasta temporária:")
print(pasta_temp)

print()

# Conta os itens
quantidade = 0

for item in pasta_temp.iterdir():
    quantidade += 1


print(f"Itens encontrados: {quantidade}")