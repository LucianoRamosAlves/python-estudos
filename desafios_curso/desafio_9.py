custo = float(input('digite o valor do custo'))
frete = float(input('digite o valor do frete'))

valor_Com_Frete = custo - frete

imposto = 15
Valor_Sem_Imposto = valor_Com_Frete
Valor_Com_Imposto = Valor_Sem_Imposto - (imposto/100) * Valor_Sem_Imposto


desconto = 5
valor_Sem_Desconto = Valor_Com_Imposto
valor_Com_Desconto = valor_Sem_Desconto - (desconto/100) * valor_Sem_Desconto


print(f' a tabela de preço')
print("-"*30)
print(f' o valor de R$:{custo} reais , menos o frete de R$:{frete} reais  fica R$:{valor_Com_Frete} reais')
print("-"*50)
print(f'retirando o imposto de {imposto}% fica R$:{Valor_Com_Imposto} reais')
print('-'*70)
print(f'valor final com {desconto}% de desconto fica R$:{valor_Com_Desconto} reais')