import random

computador = random.randint(1,10)
jogador = 0
tentativa = 0
while jogador != computador:

    jogador = int(input("escolha seu nemero de 1 a 10"))


    if jogador > computador:
        print("menos... tente novamento")
        tentativa += 1
    elif jogador < computador:
        print("mais... tente novamento")
        tentativa += 1
    else:
        print(f"parabens voçê ganhou com {tentativa} tentativas")

