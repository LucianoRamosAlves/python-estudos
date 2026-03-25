import string


# aqui eu crio o dicionario
cadastro = []


def validation_nome(nome):
    nome = nome.strip()
    max_caractere = 40
    min_caractere = 6
    
    erros_nome = []
    
    if len(nome) > max_caractere:
        erros_nome.append("Opss!, tamanho maximo atingindo.")
    if len(nome) < min_caractere:
        erros_nome.append("Opss!, nome muito pequeno.")
    if nome == "":
        erros_nome.append("Campo vazio inválido")
    if nome.isnumeric():
        erros_nome.append("Numeros não aceito nesse campo")
    if any(i in string.punctuation for i in nome):
        erros_nome.append("Caractere especial não aceito !")
    if any(i in string.digits for i in nome) and nome.isalnum():
        erros_nome.append("opss!, Nome com numeros não aceito")
    
    return erros_nome, len(erros_nome)

def validation_cpf(cpf):
    max_tamanho = 11
    min_tamanho  = 11
    erros_cpf = []
    
    if len(cpf) > max_tamanho or len(cpf) < min_tamanho:
        erros_cpf.append("CPF deve conter 11 digitos")
        
    if  not cpf.isnumeric():
        erros_cpf.append("Sómente numeros")
    
    return erros_cpf



def novo_cadastro():
    while True:
    
        print("\n--- CADASTRO ---")
    
        nome = input("digite seu nome")
        erros_nome, quantidade_erros = validation_nome(nome)
    
        if erros_nome:
            print(f"Corriga esses {quantidade_erros} erros encontrado: \n")
            for erro in erros_nome:
                print(f"erro: {erro}" )
            continue
        
        cpf = input("digite seu cpf")
        erros_cpf = validation_cpf(cpf)
        
        if erros_cpf:
            print(f"\nCorrija os erros:")
            for erro in erros_cpf:
                print(f"Corriga o seguinte erro:\n {erros_cpf}")
            continue
    
        usuario = {
            "nome": nome,
            "cpf": cpf
        }

        cadastro.append(usuario)
        
        sair = input("\nDeseja continuar? (s/n): ").lower()
        if sair == "n":
            break
        
def formatacao_cpf(cpf):
    inicial = cpf[:4]
    final = cpf[-2]
    
    return inicial + "***.***_" + final

def formatacao_nome(nome):
    nome_formatado = {
     k: v.capitalize()
     for k, v in cadastro.items()
     if cadastro["nome"]
    }
    
    return nome_formatado
    
    
