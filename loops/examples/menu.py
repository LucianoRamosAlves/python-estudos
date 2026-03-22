from time import sleep
n1 = int(input("primeiro numero"))
n2 = int(input("segundo  numero"))

opcao = 0
while opcao <= 5:
    sleep(0.5)
    print("""
        [1] somar
        [2] subtrair
        [3] multiplicar
        [4] ver o maior
        [5] novos numeros
        [QuaisQuer] sair """)
    
    print("*=-" * 30)

    opcao = int(input("escolha a opção"))

    if opcao == 1:
        print(f" a soma entre {n1} + {n2} é {n1 + n2}")
    elif opcao == 2:
        print(f" a subtração entre {n1} - {n2} é {n1 - n2}")
    elif opcao == 3:
        print(f" a multiplicaçaõ entre {n1} {n2} é {n1 * n2}")
    elif opcao == 4:
        if n1 > n2:
            print(f"o maior numero foi {n1}")
        elif n1 < n2:
            print(f"o maior numero foi {n2}")
        else:
            print("opss, numeros iguais")
    elif opcao == 5:
        n1 = int(input("primeiro numero"))
        n2 = int(input("segundo  numero"))
else:
    print("finalizado")
