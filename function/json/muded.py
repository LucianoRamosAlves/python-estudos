import json

#| aqui eu tenho um json com uma lista de clientes, cada cliente tem um nome, idade e cidade. Eu quero transformar esse json em um dicionário python para poder acessar os dados dos clientes.
clientes_json = '{"clientes": [ {"nome": "João", "idade": 30, "cidade": "São Paulo"}, {"nome": "Maria", "idade": 25, "cidade": "Rio de Janeiro"}, {"nome": "Pedro", "idade": 35, "cidade": "Belo Horizonte"} ] }' 

#| transformando o json em um dicionário python
clientes = json.loads(clientes_json)

for cliente in clientes["clientes"]:
    print(f"Nome: {cliente['nome']}, Idade: {cliente['idade']}, Cidade: {cliente['cidade']}")
    
#| agora eu tenho o dicionario python e quero transformar ele de volta em um json para poder salvar em um arquivo.

clientes_json_novo = json.dumps(clientes, indent=4)
with open("clientes.json", "w") as arquivo:
    arquivo.write(clientes_json_novo)