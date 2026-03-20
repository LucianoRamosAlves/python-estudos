

valor = float(input("digite o valor da comprar"))


print("""====== Pagamentos ======
        [1] Débito - sem taxa
        [2] Crédito - taxa de 1%
        [3] pix - desconto de 5%
        [qualquer] Dinheiro - sem taxa """)

opcao = int(input("escolha uma opção"))

if opcao == 1:
    print(f"valor a ser pago é {valor}")

elif opcao == 2:
    parcelar = input("deseja parcelar [s] ou [n]").lower()
    valor = valor * 1.01
    if parcelar == "s":
        q_parcelas = int(input("quantidades de parcelas ?"))
        v_parcela = valor / q_parcelas

        print(f"valor de R$: {valor} parcelado em {q_parcelas}\n fica R$: {v_parcela}")
    else:
        print(f"o valor no credito a vista {valor}")

elif opcao == 3:
    valor = valor * 0.95
    print(f"o valor com desconto no pix {valor}")

else:
    print(f"opcçao em dinheiro será de {valor}")


