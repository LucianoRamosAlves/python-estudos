# dicionário que vai armazenar as palavras e suas contagens
# exemplo: {"python": 3, "is": 2}
palavras = {}


# ===============================
# 📄 LEITURA DO ARQUIVO
# ===============================

# abre o arquivo "texto.txt" em modo leitura ("r")
# o "with" garante que o arquivo será fechado automaticamente
with open("texto.txt", "r") as textos:

    # percorre o arquivo linha por linha
    for texto in textos:

        # remove espaços extras e quebra de linha (\n)
        # e transforma tudo em minúsculo (padronização)
        texto = texto.strip().lower()

        # divide a linha em várias palavras usando espaço como separador
        # exemplo: "python is great" → ["python", "is", "great"]
        parts = texto.split(" ")

        # percorre cada palavra da linha
        for palavra in parts:

            # verifica se a palavra já existe no dicionário
            if palavra in palavras:

                # se já existe, soma +1 na contagem
                palavras[palavra] += 1

            else:
                # se não existe, cria a palavra com valor 1
                palavras[palavra] = 1


# ===============================
# 📊 MOSTRAR RESULTADO
# ===============================

print("\nContagem de palavras:")

# percorre o dicionário
for p in palavras:

    # imprime a palavra e quantas vezes apareceu
    print(f"{p}: {palavras[p]}")


# ===============================
# 🔍 PESQUISA INTERATIVA
# ===============================

# loop infinito para permitir várias consultas
while True:

    # pede uma palavra ao usuário
    # .lower() para manter padrão (evita erro de maiúscula/minúscula)
    pesquisa = input("\nDigite uma palavra (ou 'sair'): ").lower()

    # condição para sair do programa
    if pesquisa == "sair":
        print("Encerrando...")
        break

    # verifica se a palavra existe no dicionário
    if pesquisa in palavras:

        # mostra quantas vezes apareceu
        print(f"A palavra '{pesquisa}' aparece {palavras[pesquisa]} vezes")

    else:
        # caso não exista
        print("Palavra não encontrada")