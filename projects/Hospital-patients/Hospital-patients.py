from rich import print as rich_print
from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text
from time import sleep
from rich.console import Console
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

pacientes_normal = []
pacientes_prioritarios = []
pacientes_atendidos = []


with console.status("[bold green]Carregando...", spinner="dots", spinner_style="bold green") as status:
    sleep(1)

menu_painel = Panel(
    Align.center("[bold cyan]Bem-vindo ao Hospital![/]", vertical="middle"),
    box=box.DOUBLE,
    title="[bold magenta]Menu Principal[/]",
    subtitle="[bold yellow]Escolha uma opção[/]",
    style="bold blue",
    expand=True,
    border_style="blue"   
)
def adicionar_paciente():
    limpar_tela()
    nome = input("Digite o nome do paciente: ")
    tempo = int(input("Digite o tempo de espera (em minutos): "))
    prioridade = input("O paciente é prioritário? (s/n): ").lower() == 's'
    
    paciente = [nome, tempo, prioridade]
    
    if prioridade:
        pacientes_prioritarios.append(paciente)
        with console.status("[bold blue]adicionando paciente...", spinner="dots", spinner_style="bold blue") as status:
            sleep(1)
        rich_print(f"[bold green]Paciente {nome} adicionado à fila prioritária![/]")
    else:
        pacientes_normal.append(paciente)
        with console.status("[bold blue]adicionando paciente...", spinner="dots", spinner_style="bold blue") as status:
            sleep(1)
        rich_print(f"[bold green]Paciente {nome} adicionado à fila normal![/]")

def atender_paciente():
    limpar_tela()
    if pacientes_prioritarios:
        paciente = pacientes_prioritarios.pop(0)
        pacientes_atendidos.append(paciente)
        with console.status("[bold blue]atendendo paciente prioritário...", spinner="line", spinner_style="bold blue") as status:
            sleep(1)
        rich_print(f"[bold green]Paciente {paciente[0]} atendido![/]")
    elif pacientes_normal:
        paciente = pacientes_normal.pop(0)
        pacientes_atendidos.append(paciente)
        with console.status("[bold blue]atendendo paciente normal...", spinner="line", spinner_style="bold blue") as status:
            sleep(1)
        rich_print(f"[bold green]Paciente {paciente[0]} atendido![/]")
    else:
        rich_print("[bold red]Não há pacientes para atender![/]")

def listar_pacientes():
    limpar_tela()
    with console.status("[bold blue]listando pacientes...", spinner="arc", spinner_style="bold blue") as status:
            sleep(1)
    if not pacientes_prioritarios and not pacientes_normal:
        rich_print("[bold red]Não há pacientes na fila![/]")
        return
    
    rich_print("[bold cyan]Pacientes Prioritários:[/]")
    for paciente in pacientes_prioritarios:
        rich_print(f"- {paciente[0]} (Tempo de espera: {paciente[1]} minutos)")
    
    rich_print("\n[bold cyan]Pacientes Normais:[/]")
    for paciente in pacientes_normal:
        rich_print(f"- {paciente[0]} (Tempo de espera: {paciente[1]} minutos)")

def buscar_paciente():
    limpar_tela()
    nome = input("Digite o nome do paciente que deseja buscar: ")

    with console.status("[bold blue]buscando paciente...", spinner="circle", spinner_style="bold blue") as status:
            sleep(1)
    
    for paciente in pacientes_prioritarios + pacientes_normal:
        if paciente[0].lower() == nome.lower():
            rich_print(f"[bold green]Paciente encontrado: {paciente[0]} (Tempo de espera: {paciente[1]} minutos, Prioritário: {'Sim' if paciente[2] else 'Não'})[/]")
            return
    
    rich_print("[bold red]Paciente não encontrado![/]")
    


opcao = None
while True:
    rich_print(menu_painel)
    rich_print("[bold yellow]1.[/] :heavy_plus_sign: adicionar paciente")
    rich_print("[bold yellow]2.[/] :stethoscope: Atender paciente")
    rich_print("[bold yellow]3.[/] :clipboard: Listar pacientes")
    rich_print("[bold yellow]4.[/] :magnifying_glass_tilted_left: buscar paciente")
    rich_print("[bold yellow]0.[/] :door: Sair")
    try:
        opcao = int(input("Escolha sua opção [0] a [5] "))
    except ValueError:
        limpar_tela()
        rich_print(" [red b  bold ] Opção inválida! Tente Novamente [/]")
        continue

    if opcao == 0:
        rich_print("[bold red] :door: Saindo do sistema...  [/]")
        break

    elif opcao == 1:
        adicionar_paciente()

    elif opcao == 2:
        atender_paciente()

    elif opcao == 3:
        listar_pacientes()

    elif opcao == 4:
        buscar_paciente()

    else:
        limpar_tela()
        rich_print("[bold red]Opção inválida! Tente novamente.[/]")
