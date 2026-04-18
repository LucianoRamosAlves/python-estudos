
words = {}
with open("dicionario.txt", "r") as caderno:
    for linha in caderno:
        linha = linha.strip()
        parts = linha.split(" ") # aqui eu divido por espaços -> "a b" -- ["a",  "b"]
        if len(parts) == 2:
            words[parts[0]] = parts[1]
while True:
    word = input("digite algo: ")

    if word in words:
        print(words[word])
    else:
        print("não achei")

