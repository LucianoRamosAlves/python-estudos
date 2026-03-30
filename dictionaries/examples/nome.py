# Inicializa uma lista vazia para armazenar os nomes dos usuários

nomes = []
# Define uma função para adicionar um novo nome à lista
def adicionar_nome():
    nomes.clear()
    nome = input("Digite seu nome: ")
    nomes.append(nome)
    print(nome + " adicionado com sucesso!")


# Define uma função que retorna o nome abreviado (primeira letra do primeiro nome + primeira letra do último nome)
def nome_abreviado(nome):
    tamanho = len(nome)
    tamanho_minimo = 3
    # Divide o nome em partes separadas por espaço
    partes = nome.split()
    # Verifica se o nome tem pelo menos 2 partes (nome e sobrenome)
    if len(partes) == 2 and tamanho >= tamanho_minimo:
        # Cria a abreviação: primeira letra do primeiro nome + ponto + primeira letra do último nome + ponto
        abreviado = partes[0][0] + ". " +  partes[-1][0] + "."
        # Retorna a abreviação
        return abreviado
    elif len(partes) == 3 and tamanho >= tamanho_minimo:
        # Cria a abreviação: primeira letra do primeiro nome + ponto + primeira letra do último nome + ponto
        abreviado = partes[0][0] + ". " + partes[1][0] + ". " + partes[-1][0] + "."
        return abreviado
    elif len(partes) >= 4 and tamanho >= tamanho_minimo:
        # Cria a abreviação: primeira letra do primeiro nome + ponto + primeira letra do último nome + ponto
        abreviado = partes[0][0] + ". " + partes[1][0] + ". " + partes[2][0] + ". " + partes[-1][0] + "."
        # Retorna a abreviação
        # Retorna a abreviação
        return abreviado
    else:
        # Se o nome tem apenas uma parte, retorna o nome original
        return nome
    
# Define uma função que formata o nome substituindo letras por asteriscos
def nome_formatado(nome):
    # Divide o nome em partes separadas por espaço
    partes = nome.split()
    # Formata cada parte do nome: primeira letra + 4 asteriscos, depois junta com espaço
    formatado = " ".join([parte[0] + "****" for parte in partes])
    # Retorna o nome formatado
    return formatado

# Inicia um loop infinito para o menu principal
while True:
    # Exibe o menu principal com as opções disponíveis
    print("""
          --- MENU ---
          (1). Formatar nome
          (2). adicionar nome
          (3). Sair""")
    # Solicita ao usuário que escolha uma opção
    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida. Tente novamente.")
        continue

    # Verifica se a opção escolhida é 1 (Formatar nome)
    if opcao == 1:
        # Exibe o submenu de formatação de nome
        print("""
              --- FORMATAÇÃO DE NOME ---
        (1). Abreviado
        (2). a**** b****
        (3). voltar ao menu principal""")
        # Solicita ao usuário que escolha uma opção de formatação
        try:
            opcao_formatacao = int(input("Escolha uma opção de formatação: "))
        except ValueError:
            print("Opção de formatação inválida. Voltando ao menu principal.")
            continue

        # Verifica se a opção de formatação é 1 (Abreviado)
        if opcao_formatacao == 1:
            # Itera sobre cada nome na lista de nomes
            for nome in nomes:
                # Imprime o nome abreviado
                print(nome_abreviado(nome))
        # Verifica se a opção de formatação é 2 (a**** b****)
        elif opcao_formatacao == 2:
            # Itera sobre cada nome na lista de nomes
            for nome in nomes:
                # Imprime o nome formatado
                print(nome_formatado(nome))
        # Verifica se a opção de formatação é 3 (voltar ao menu principal)
        elif opcao_formatacao == 3:
            # Continua o loop, voltando ao menu principal
            continue
        else:
            # Se a opção de formatação é inválida, exibe mensagem de erro
            print("Opção de formatação inválida. Voltando ao menu principal.")
    # Verifica se a opção escolhida é 2 (adicionar nome)
    elif opcao == 2:
        # Chama a função para adicionar um novo nome
        adicionar_nome()
    # Verifica se a opção escolhida é 3 (Sair)
    elif opcao == 3:
        # Exibe mensagem de saída
        print("Saindo do programa...")
        # Encerra o loop e o programa
        break
    else:
        # Se a opção é inválida, exibe mensagem de erro
        print("Opção inválida. Tente novamente.")