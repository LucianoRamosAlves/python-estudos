from operator import itemgetter

pacientes = []

def adicionar():
    while True:
        while True:
            nome = str(input("Digite o nome do Paciente: ")).capitalize()
            if nome.strip() and nome.isalpha():
                break
            print("Nome inválido. Digite um nome válido.")

        while True:
            try:
                idade = int(input("Digite a idade do Paciente: "))
                if 0 < idade < 150:
                    break
                print("Idade inválida. Digite um valor entre 1 e 149.")
            except ValueError:
                print("Idade inválida. Digite um número.")

        paciente = {
            "nome": nome,
            "idade": idade
        }

        pacientes.append(paciente)

        while True:
            opcao = str(input("Adicionar um novo paciente? [s]/[n]: ")).lower()
            if opcao in ["s", "n"]:
                break
            print("Opção inválida. Digite 's' ou 'n'.")

        if opcao == "n":
            break


def mostrar():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    for i, item in enumerate(pacientes):
        print(f'Paciente número {i+1}: nome {item["nome"]} idade: {item["idade"]} anos')


def organizar_idade():
    if not pacientes:
        print("Nenhum paciente para organizar.")
        return []
    pacientes_organizados = sorted(pacientes, key=itemgetter('idade'), reverse=True)
    for i, item in enumerate(pacientes_organizados):
        print(f'{item["idade"]} anos, nome {item["nome"]}')
    return pacientes_organizados


def proximo(pacientes_organizados):
    if not pacientes_organizados:
        print("Nenhum paciente disponível.")
        return None
    if not hasattr(proximo, 'iterador'):
        proximo.iterador = iter(pacientes_organizados)
    try:
        return next(proximo.iterador)
    except StopIteration:
        print("Não há mais pacientes.")
        proximo.iterador = iter(pacientes_organizados)


def menu():
    pacientes_organizados = []
    while True:
        print("\n=== MENU ===")
        print("1. Adicionar paciente")
        print("2. Mostrar pacientes")
        print("3. Organizar por idade")
        print("4. Próximo paciente")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar()
        elif opcao == "2":
            mostrar()
        elif opcao == "3":
            pacientes_organizados = organizar_idade()
        elif opcao == "4":
            proximo(pacientes_organizados)
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


menu()
