valor_casa = float(input("qual o valor da casa ?"))
salario = float(input("qual o valor do seu salario ?"))
q_parcela = float(input("quantidades de parcelas em anos ?"))

parcelas = valor_casa / (q_parcela * 12 )
limite = salario * 0.3

if not parcelas >= limite:
    print(f"emprestimo concebido valor de cada parcela {parcelas}")
else:
    print("emprestimo negado")

