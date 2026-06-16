import pandas as pd

from tabulate import tabulate



def print_df(df):
    if isinstance(df, pd.Series):
        df = df.to_frame()

    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

# se caso tiver caracteres ao invés de números, posso usar o parâmetro encoding para especificar a codificação do arquivo csv

# os codigos mais comuns são:
# utf-8: é a codificação mais comum e amplamente utilizada, suporta uma ampla variedade de caracteres e é compatível com a maioria dos sistemas.
# latin-1 (ou iso-8859-1): é uma codificação que suporta caracteres acentuados comuns em idiomas ocidentais, como português, espanhol e francês. É útil quando o arquivo csv contém caracteres acentuados.

vendas = pd.read_csv(r'C:\Users\lramo\OneDrive\Documentos\GitHub\python-estudos\file\docs\Contoso - Vendas - 2017.csv', sep=';', encoding='ISO-8859-1') # o sep é para especificar o separador do arquivo csv, nesse caso é o ponto e vírgula (;)

produtos = pd.read_csv(r'C:\Users\lramo\OneDrive\Documentos\GitHub\python-estudos\file\docs\Contoso - Cadastro Produtos.csv', sep=';', encoding='ISO-8859-1')


lojas = pd.read_csv(r'C:\Users\lramo\OneDrive\Documentos\GitHub\python-estudos\file\docs\Contoso - Lojas.csv', sep=';', encoding='ISO-8859-1')

clientes = pd.read_csv(r'C:\Users\lramo\OneDrive\Documentos\GitHub\python-estudos\file\docs\Contoso - Clientes.csv', sep=';', encoding='ISO-8859-1')

for df in [vendas, produtos, lojas, clientes]:
    df.columns = df.columns.str.replace('ÿ', '', regex=False)

# print_df(vendas.head())
# print_df(clientes.head())

# posso usar o drop para remover colunas

clientes = clientes.drop(columns=['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10'])
#print_df(clientes.head())

# ou posso peggar as colunas

### pego os nomes das colunas se preciso
# print(produtos.columns.tolist()) pego as colunas do dataframe e transformo em uma lista
# print(clientes.columns.tolist())
# print(lojas.columns.tolist())

## junto as colunas que me interessam
clientes = clientes[['ID Cliente','E-mail']]
produtos = produtos[['ID Produto', 'Nome do Produto']]
lojas = lojas[['ID Loja', 'Nome da Loja']]

# print_df(produtos.head())
# print_df(lojas.head())

# agora vou juntar em outra tabela

vendas_df = vendas.merge(clientes, on='ID Cliente')
vendas_df = vendas_df.merge(produtos, on='ID Produto')
vendas_df = vendas_df.merge(lojas, on='ID Loja')

vendas_df = vendas_df.rename(columns={'E-mail': 'Email do Cliente'})

# print_df(vendas_df.head())

frequencia_clientes = vendas_df['Email do Cliente'].value_counts().reset_index()
#print_df(frequencia_clientes.head())

frequencia_clientes[:5].plot(figsize=(15, 5))


