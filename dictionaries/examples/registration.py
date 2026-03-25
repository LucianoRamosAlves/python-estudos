import string


# aqui eu crio o dicionario
cadrasto = dict.fromkeys(["nome", "cpf"], None)

def validation_nome(nome):
    nome = nome.strip()
    max_caractere = 40
    min_caractere = 6
    
    erros = []
    
    if len(nome) > max_caractere:
        erros.append("Opss!, tamanho maximo atingindo.")
    if len(nome) < min_caractere:
        erros.append("Opss!, nome muito pequeno.")
    if nome == "":
        erros.append("Campo vazio inválido")
    if nome.isnumeric():
        erros.append("Numeros não aceito nesse campo")
    if any(i in string.punctuation for i in nome):
        erros.append("Caractere especial não aceito !")
    if any(i in string.digits for i in nome) and nome.isalnum():
        erros.append("opss!, Nome com numeros não aceito")
    
    return erros, len(erros)
    
    

while True:
    
    print("\n--- CADASTRO ---")
    
    nome = input("digite seu nome")
    
    erros, quantidade_erros = validation_nome(nome)
    
    if erros:
        print(f"Corriga esses {quantidade_erros} erros encontrado: \n")
        for erro in erros:
            print(f"erro: {erro}" )
    else:
        cadrasto["nome"] = nome
        print(cadrasto)