from rich import print as rich_print
import msvcrt
import time
from rich.console import Console
import string
from datetime import datetime
import random

codigos = []
def pre_fixo_cod(tipo_produto):
    primeira_letra = tipo_produto[0]
    ultima_letra = tipo_produto[-1]
    tamanho = len(tipo_produto)

    prefixo = f"{primeira_letra}{ultima_letra}{tamanho}"
    return prefixo


def data_hora():
    agora = datetime.now()
    codigo_data = agora.strftime("%y%m%d%H%M%S")
    return codigo_data

def cod_aleatorio():
    codigo_aleatorio = [
        random.choice(string.digits),
        random.choice(string.ascii_letters),
        random.choice(string.punctuation)
    ]

    possibilidades = "".join([string.digits, string.ascii_letters, string.punctuation])
    codigo_aleatorio += random.choices(possibilidades, k=7)

    random.shuffle(codigo_aleatorio)

    return "".join(codigo_aleatorio)

def codigo_final():
    possibilidades = string.punctuation
    codigo_aleatorio = random.choice(possibilidades)
    codigo_aleatorio1 = random.choice(possibilidades)

    codigo = f"{tipo}{codigo_aleatorio}{data_hora()}{codigo_aleatorio1}{cod_aleatorio()}"
    return codigo

def carregamento_c():
    with console.status("[bold green]Gerando Codigo...", spinner="dots", spinner_style="bold green") as status:
        time.sleep(2)

def mostrar_c():
    c = codigo_final()
    carregamento_c()
    rich_print(f"""
               [bold][green] Codigo criado com Suscesso [/bold][/green]
                {c}
                """)
    codigos.append(c)
    print(codigos)



rich_print(" Bem VINDO ao [bold][purple] COD.COM [/purple][/bold]")

time.sleep(1)

console = Console()

time.sleep(2)
with console.status("[bold purple]Carregando...", spinner="aesthetic", spinner_style="bold purple") as status:
    rich_print("""
               [bold][yellow] Avisos ![/yellow][/bold]
               [bold] Gere seu código com muito mais [purple]eficiência [/purple][/bold]
               """)
    time.sleep(2)

    rich_print("[bold] Use o [purple]COD.COM[/purple] para acelerar seu desenvolvimento![/bold]")
    time.sleep(2)

    rich_print("[bold] Saia na [purple]Frente[/purple] com o COD.COM![/bold]")
    time.sleep(2)

print("Pressione qualquer tecla para continuar...")
msvcrt.getch()

def carregamento():
    with console.status("[bold purple]Carregando...", spinner="arc", spinner_style="bold purple") as status:
        time.sleep(2)
while True:
    rich_print("[bold][green] Bem Vindo(a) [/green] [purple] COD.COM [/purple][/bold]")
    rich_print(f"[bold]{time.strftime('%Y-%m-%d %H:%M:%S')}[/bold]")

    carregamento()

    rich_print("""
    [bold][purple] Opções Disponíveis: [/purple][/bold]
    [bold][purple] 1. [/purple]Gerar Código[/bold]
    [bold][purple] 2. [/purple]Sair[/bold]
               """)

    opcao = input("Escolha o que deseja fazer: ")

    if opcao == "1":
        while True:

            rich_print("""
            [bold][purple] Opções Disponíveis: [/purple][/bold]
            [bold][purple] 1. [/purple]Eletronicos[/bold]
            [bold][purple] 2. [/purple]Roupas[/bold]
            [bold][purple] 3. [/purple]Assessorios[/bold]
            [bold][purple] 4. [/purple]Peças Intimas[/bold]
            [bold][purple] 5. [/purple]Variados[/bold]
            [bold][purple] 6. [/purple]Relogios[/bold]
            [bold][red] 7. [/red]Voltar[/bold]
            """)

            categorias = {
                "1": "Eletronicos",
                "2": "Roupas",
                "3": "Assessorios",
                "4": "Peças Intimas",
                "5": "Variados",
                "6": "Relogios"
            }

            tipo_mercadoria = input("Escolha o tipo da mercadoria: ")

            if tipo_mercadoria == "7":
                break

            elif tipo_mercadoria in categorias:
                nome = categorias[tipo_mercadoria]

                rich_print(
                    f"[bold yellow]Confirmar criar código para {nome}: [S]/[N][/bold yellow]"
                )

                confirmar = input().lower()

                if confirmar == "s":
                    tipo = pre_fixo_cod(nome).lower()
                    mostrar_c()

                elif confirmar == "n":
                    continue

                else:
                    rich_print(
                        "[bold yellow]Opção inválida! Digite S ou N.[/bold yellow]"
                    )

            else:
                rich_print(
                    "[bold yellow]Opção inválida! Tente novamente [1] a [7].[/bold yellow]"
                )

    
    elif opcao == "2":
        rich_print("[bold][red] Realmente deseja Sair ?: [S]/[N][/red][/bold]")
        confimar = input().lower() 

        if confimar == "s":
            rich_print("[bold][red] Saindo... [/red][/bold]")
            carregamento()
            rich_print("[bold][red] Até logo! [/red][/bold]")
            break

        elif confimar == "n":
            continue

        else:
            rich_print("[bold][yellow] Opção Inválida! Tente Novamente [S] ou [N].[/yellow][/bold]")
            continue 

    else:
        rich_print("[bold][yellow] Opção Inválida! Tente Novamente [1] ou [2].[/yellow][/bold]")
        continue

