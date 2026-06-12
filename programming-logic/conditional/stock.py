print(" olá, digite seu nome abaixo: ")
nome = input()
produto = input(" digite o nome do produto: ")

categoria = input(" digite a categoria do produto: ")

quantidade = input(" digite a quantidade do produto: ")

# quantidades em estoques
alimentos = 50
bebidas = 75
limpeza = 30

if produto and categoria and quantidade:

    int(quantidade)

    if categoria == "alimentos":
        if quantidade > 50:
            msg = "disponivél em abudancia no estoque"
        elif quantidade == 50:
           msg = "em estoque mas, fique atento nos proximos dias"
        else:
            msg = "solicitar reposisão"

    if categoria == "bebidas":
        if quantidade > 75:
            msg = "disponivél em abudancia no estoque"
        elif quantidade == 75:
            msg = "em estoque mas, fique atento nos proximos dias"
        else:
            msg = "solicitar reposisão"

    if categoria == "limpeza":
        if quantidade > 30:
            msg = "disponivél em abudancia no estoque"
        elif quantidade == 30:
            msg = "em estoque mas, fique atento nos proximos dias"
        else:
            msg = "solicitar reposisão"

    print(f"""
        Funcionario {nome}:

        produto: {produto}

        Status no estoque: {msg}

""")
    
else:
    print("oppss.. algum campo ficou incorrreto, tente novamente :) ")

    

