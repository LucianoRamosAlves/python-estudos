nomes = ['pedro', 'maria', 'cassio', '', 'paulo']

#| break, isso para o for e executa até ali
print("BREAK")
for nome in nomes:
    if nome == "":
        print("nome vazio encontrado")
        break
    #| sem o break, o nome vazio ia executar
    print(f"nome = {nome}")

print("=-" * 40)
#** continue, se verdade, ele pula a rodada e vai para a proxima
print("CONTINUE")
for nome in nomes:
    if nome == "":
        print("nome vazio encontrado")
        continue
    #| continue, tem o vazio, ele pula e continua
    print(f"nome = {nome}")
