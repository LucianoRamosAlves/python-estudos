import pandas as pd

vendas = pd.read_csv(r'C:\Users\lramo\OneDrive\Documentos\GitHub\python-estudos\file\docs\Contoso - Vendas - 2017.csv', sep=';')

#print(vendas[:0]) # mostra as colunas do arquivo csv

#print(vendas.head()) # mostra as 5 primeiras linhas do arquivo csv

#print(vendas.tail()) # mostra as 5 ultimas linhas do arquivo csv

#print(vendas[['Data da Venda', 'ID Cliente']]) # mostra as colunas "Data da Venda" e "ID Cliente" do arquivo csv

print(vendas.info()) # mostra informações sobre o arquivo csv, como o número de linhas, colunas e tipos de dados.

# posso cruar um novo arquivo csv a partir do arquivo original, selecionando apenas as colunas "Data da Venda" e "ID Cliente"
vendas_selecionadas = vendas[['Data da Venda', 'ID Cliente']]

print(vendas_selecionadas)
