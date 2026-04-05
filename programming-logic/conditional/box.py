# melhorar os nomes das cores.. colocar o nome real


V = "\033[31m"
v = "\033[32m"
a = "\033[33m"
A = "\033[34m"
reset = "\033[m"

print( A + '=== CAIXA DO MERCADO ===' + reset)

produto = input('Digite um produto').lower()


validor = True

if produto == 'arroz':
   preco =  10

elif produto == 'feijão':
    preco = 7

elif produto == 'café':
    preco = 14.5

elif produto == 'açucar':
    preco = 3.0

elif produto == 'sal':
    preco = 8.0

else:
    print( V + 'opss!! produto fora de estoque.' + reset)
    validor = False



if validor :
    quantidade = float(input('digite a quantidade'))

    if quantidade <= 0:
       valor = 0
       print(V + 'quantidade inválida' + reset)
       validor = False
    else:
       valor = quantidade * preco

    clube = input('faz parte do clube ?').lower()



    if clube == 'sim':
     desconto = valor * 0.9
     print( v + 'O valor da sua compra com 10% de desconto foi R${:.2f}'.format(desconto) + reset)

    else:
     print( a +  'total a pagar R${:.2f}'.format(valor) + reset) 



