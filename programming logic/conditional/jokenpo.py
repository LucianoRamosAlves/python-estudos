import random
import time

print(""" sua jogada
        [0] pedra
        [1] papel
        [2] tesoura""")
jogagor_a = int(input("escolha uma opção"))

jogagor_b = random.randint(0,2)

def converter(valor):
    if valor == 0:
        return "pedra"
    elif valor == 1:
        return "papel"
    else:
        return "tesoura"
    
print("JO ")
time.sleep(1)
print("KEN")
time.sleep(1)
print("PO")


if ((jogagor_a == 0) and (jogagor_b == 2)) or ((jogagor_a == 1) and (jogagor_b == 0)) or ((jogagor_a == 2) and (jogagor_b == 1)):
    print(f"parabens voce ganhou :) sua jogada {converter(jogagor_a)}\n jogada do computador {converter(jogagor_b)}")

elif jogagor_a == jogagor_b:
    print("jogo empatado")

else:
    print(f"que pena. voce perdeu :( sua jogada {converter(jogagor_a)}\n jogada do computador {converter(jogagor_b)}") 