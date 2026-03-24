print('===== CADRASTO DE PESSOA =====')

nome = []
idade = []
nome_grup20 = []
idade_grup20 = []
nome_grup60 = []
idade_grup60 = []


while True:

    print("""--- MENU PRINCINPAL ---
        
        [1] Consultas 
        [2] Quantidades
        [3] Status
        [4] Adicionar
        [5] Remover
        [6] Sair
    

        """)

    
    option_menu_principal = int(input("Escolha a opção: [1] a [6]"))
    
    if option_menu_principal == 1:
        while True:
            print("""
        --- Menu de Consultas ---
        [1] Ver todos
        [2] ver grupo +20
        [3] ver grupo +60
        [4] sair""")
            option_menu_consultar = int(input("Escolha a opção: [1] a [4]")) 
            
            
            if option_menu_consultar == 1:
                print("TABELA GERAL")
                for n, i in zip(nome, idade):
                    print(f"Nome: {n} sua idade {i}")
                
                
            elif option_menu_consultar == 2:
                print("TABELA GRUPO MAIS 20")
                for n, i in zip(nome_grup20, idade_grup20):
                    print(f"Nome: {n} sua idade {i}")
                
            elif option_menu_consultar == 3:
                print("TABELA GERAL")
                for n, i in zip(nome_grup60, idade_grup60):
                    print(f"Nome: {n} sua idade {i}")

            elif option_menu_consultar == 4:
                break

            else:
                print("opção inválida, tente novamente") 
                
                
                
                
                
                
    elif option_menu_principal == 3:
        while True:
            print("""
        --- Menu Quantidade ---
        [1] Total de pessoas
        [2] quantidade grupo +20
        [3] quantidade +60
        [4] sair""")
            option_menu_quantidade = int(input("Escolha a opção: [1] a [4]"))
            
            
            if option_menu_quantidade == 1:
                print("Quantidade Geral")
                q_total = len(idade)
                
                print(f"Atualmente temos {q_total} pessoas no grupo")
                
                
            elif option_menu_quantidade == 2:
                q_total = len(idade_grup20)
                
                print(f"Atualmente temos {q_total} pessoas no grupo mais 20")
                
            elif option_menu_quantidade == 3:
                q_total = len(idade_grup60)
                
                print(f"Atualmente temos {q_total} pessoas no grupo mais 60")
                
            elif option_menu_quantidade == 4:
                break

            else:
                print("opção inválida, tente novamente") 
                
                
        
    elif option_menu_principal == 4:
        while True:
            print("""
                  
            --- Menu Adicionar ---
            [1] adicionar no geral
            [2] Adicionar no grupo +20
            [3] Adicionar no grupo +60
            [4] Voltar""")

            option_menu_adicionar = int(input("Escolha a opção: [1] a [4]"))

            if option_menu_adicionar == 1:
                n_nome = str(input("digite seu nome:"))
                n_idade = int(input("digite  sua idade:"))
                
                if not isinstance(nome, str) or isinstance(idade, int):
                    print("opss! nome ou idade incorreto, tente novamente")
                else:
                    nome.append(n_nome)
                    idade.append(n_idade)

            elif option_menu_adicionar == 2:
                n_nome = str(input("digite seu nome:"))
                n_idade = int(input("digite  sua idade:"))

                nome_grup20.append(n_nome)
                idade_grup20.append(n_idade)
                nome.append(n_nome)
                idade.append(n_idade)

            elif option_menu_adicionar == 3:
                n_nome = str(input("digite seu nome:"))
                n_idade = int(input("digite  sua idade:"))

                nome_grup60.append(n_nome)
                idade_grup60.append(n_idade)
                nome.append(n_nome)
                idade.append(n_idade)
                                

            elif option_menu_adicionar == 4:
                break

            else:
                print("opção inválida, tente novamente")
                
# BUG  falta terminar, melhorar validação
                        

                        
                        
                        
                        
                        