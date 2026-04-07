from rich import print
from rich.panel import Panel
import time
from rich.progress import track
import random


class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[" ", " ", " "] for _ in range(3)]
        self.jogadas = 0
        self.quemjoga = "X"
        self.vitorias = False
        self.modo_cpu = False

    def exibir_tabuleiro(self):
        print("  1   2   3")
        for i in range(3):
            print(f"{i+1} {self.tabuleiro[i][0]} | {self.tabuleiro[i][1]} | {self.tabuleiro[i][2]}")
            if i < 2:
                print("  ---+---+---")
        print(f"Jogadas: [blue]{self.jogadas}[/blue]")
        print(Panel.fit(f"Vez do jogador [red]{self.quemjoga}[/red]"))

    def verificar_vitoria(self):
        for i in range(3):
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] != " ":
                return True
            if self.tabuleiro[0][i] == self.tabuleiro[1][i] == self.tabuleiro[2][i] != " ":
                return True
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != " ":
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != " ":
            return True
        return False

    def resetar(self):
        self.tabuleiro = [[" ", " ", " "] for _ in range(3)]
        self.jogadas = 0
        self.quemjoga = "X"
        self.vitorias = False

    def jogar_turno(self):
        if self.modo_cpu and self.quemjoga == "O":
            linha, coluna = random.randint(0, 2), random.randint(0, 2)
        else:
            linha = int(input("Linha (1-3): ")) - 1
            coluna = int(input("Coluna (1-3): ")) - 1

        if 0 <= linha < 3 and 0 <= coluna < 3 and self.tabuleiro[linha][coluna] == " ":
            self.tabuleiro[linha][coluna] = self.quemjoga
            self.jogadas += 1
            self.exibir_tabuleiro()
            if self.verificar_vitoria():
                self.vitorias = True
            else:
                self.quemjoga = "O" if self.quemjoga == "X" else "X"
        else:
            print("[red]Posição inválida.[/red]")
    


def exibir_mensagem(mensagem):
    print(Panel.fit(mensagem))
    time.sleep(1)
    


while True:
    print(Panel.fit("O que deseja fazer?"))
    print("[1] Iniciar jogo")
    print("[2] Encerrar jogo")
    escolha = input("Digite sua escolha: ")
    if escolha == "1":
        for i in track(range(100), description="Carregando o jogo..."):
            time.sleep(0.05)
        print("[1] jogar contra outro jogador")
        print("[2] jogar contra a CPU")
        modo = input("Escolha o modo de jogo: ")
        if modo == "1":
            jogo = JogoDaVelha()
            jogo.exibir_tabuleiro()
            while not jogo.vitorias and jogo.jogadas < 9:
                jogo.jogar_turno()
            if jogo.vitorias:
                print(Panel.fit(f"Jogador [red]{jogo.quemjoga}[/red] venceu!"))
            else:
                print(Panel.fit("Empate!"))
        elif modo == "2":
            jogo = JogoDaVelha()
            jogo.modo_cpu = True
            jogo.exibir_tabuleiro()
            while not jogo.vitorias and jogo.jogadas < 9:
                jogo.jogar_turno()
            if jogo.vitorias:
                print(Panel.fit(f"Jogador [red]{jogo.quemjoga}[/red] venceu!"))
            else:
                print(Panel.fit("Empate!"))
                
        else:
            exibir_mensagem("Opção inválida. Tente novamente.")
            time.sleep(1)
    elif escolha == "2":
        exibir_mensagem("Encerrando o jogo...")
        break
    else:
        exibir_mensagem("Opção inválida. Tente novamente.")
        time.sleep(1)



    
