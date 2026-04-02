

print("""--- Bem vindo ao Quiz de Programação Lógica ---
      Responda as perguntas abaixo para testar seus conhecimentos!
      cada resposta correta vale 2 pontos, e cada resposta incorreta vale 0 pontos.
      Boa sorte!""")

# Define as perguntas e respostas do quiz
pergunta1 = input("1. Existe a linguagem de programação chamada 'Python'? (Sim/Não) ").lower()

pergunta2 = input("2. O que é uma variável em programação? (a) Um tipo de dado, (b) Um espaço na memória para armazenar valores, (c) Um operador lógico ").lower()

pergunta3 = input("3. O que é um loop em programação? (a) Uma estrutura de controle que repete um bloco de código, (b) Um tipo de função, (c) Um erro de sintaxe ").lower()

pergunta4 = input("4. Quanto equivale em minutos 1.5 horas? (a) 90 minutos, (b) 60 minutos, (c) 120 minutos ").lower()

pergunta5 = input("5. O que é um algoritmo? (a) Um conjunto de instruções para resolver um problema, (b) Um tipo de dado, (c) Um erro de sintaxe ").lower()

# Inicializa a pontuação do quiz
pontuacao = 0
quantidades_acertos = 0


if pergunta1 == "sim":
    pontuacao += 2
    quantidades_acertos += 1
    
if pergunta2 == "b":
    pontuacao += 2
    quantidades_acertos += 1

if pergunta3 == "a":
    pontuacao += 2
    quantidades_acertos += 1

if pergunta4 == "a":
    pontuacao += 2
    quantidades_acertos += 1

if pergunta5 == "a":
    pontuacao += 2
    quantidades_acertos += 1
    
porcentagem_acerto = (quantidades_acertos * 100) / 5
porcentagem_erro = 100 - porcentagem_acerto

status = "Aprovado" if porcentagem_acerto >= 60 else "Reprovado"


print(f"Você acertou {quantidades_acertos} perguntas, totalizando {pontuacao} pontos.")
print(f"Sua porcentagem de acertos foi de {porcentagem_acerto:.2f}% e a porcentagem de erros foi de {porcentagem_erro:.2f}%.")
print(f"Status: {status}")
