import random

nomes = [
    "joao", "maria", "pedro", "ana", "carlos",
    "lucas", "fernanda", "julia", "rafael", "bruno"
]

dominios = [
    "gmail.com",
    "hotmail.com",
    "yahoo.com",
    "outlook.com"
]

emails = []

for i in range(500):
    nome = random.choice(nomes)
    numero = random.randint(1, 9999)

    tipo = random.randint(1, 10)

    if tipo <= 5:
        # válido
        email = f"{nome}{numero}@{random.choice(dominios)}"

    elif tipo == 6:
        # sem @
        email = f"{nome}{numero}{random.choice(dominios)}"

    elif tipo == 7:
        # sem domínio
        email = f"{nome}{numero}@"

    elif tipo == 8:
        # suspeito
        email = f"spam_{nome}{numero}@gmail.com"

    elif tipo == 9:
        # duplicado
        email = "joao123@gmail.com"

    else:
        # caracteres estranhos
        email = f"$$${nome}{numero}@gmail.com"

    emails.append(email)

with open("emails.txt", "w", encoding="utf-8") as arquivo:
    for email in emails:
        arquivo.write(email + "\n")

print(emails)