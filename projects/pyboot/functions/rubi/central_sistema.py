import os

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.align import Align

console = Console()


def bloquear_computador():

    console.print()
    console.print("[bright_cyan]●[/] Bloqueando computador...")

    os.system("rundll32.exe user32.dll,LockWorkStation")


def reiniciar_computador():

    console.print()

    confirmar = Confirm.ask("[bold yellow]Deseja realmente reiniciar o computador?[/]")

    if not confirmar:
        console.print("\n[dim]Reinicialização cancelada.[/]")
        return

    console.print()
    console.print("[bright_cyan]●[/] Reiniciando computador...")

    os.system("shutdown /r /t 0")


def desligar_computador():

    console.print()

    confirmar = Confirm.ask("[bold yellow]Deseja realmente desligar o computador?[/]")

    if not confirmar:
        console.print("\n[dim]Desligamento cancelado.[/]")
        return

    console.print()
    console.print("[bright_cyan]●[/] Desligando computador...")

    os.system("shutdown /s /t 0")


def agendar_desligamento():

    console.print()

    minutos = Prompt.ask("[bold bright_cyan]Desligar daqui a quantos minutos? ❯[/]")

    # =========================
    # VALIDAR
    # =========================

    if not minutos.isdigit():

        console.print()
        console.print("[bold red]✕ Digite apenas números.[/]")

        return

    minutos = int(minutos)

    if minutos <= 0:

        console.print()
        console.print("[bold red]✕ Digite um tempo maior que zero.[/]")

        return

    # =========================
    # CONVERTER PARA SEGUNDOS
    # =========================

    segundos = minutos * 60

    # =========================
    # AGENDAR
    # =========================

    os.system(f"shutdown /s /t {segundos}")

    console.print()

    console.print(
        "[bright_green]✓[/] "
        f"[bold white]Desligamento agendado para "
        f"daqui a {minutos} minuto(s).[/]"
    )


def cancelar_desligamento():

    console.print()

    os.system("shutdown /a")

    console.print()

    console.print(
        "[bright_green]✓[/] " "[bold white]Comando de cancelamento enviado.[/]"
    )


def central_sistema():

    while True:

        console.clear()

        # =========================
        # TÍTULO
        # =========================

        titulo = Panel(
            "[bold white]CENTRAL DO SISTEMA[/]\n"
            "[dim]Controle funções do Windows pelo PyBoot.[/]",
            title="[bold bright_red]◆ RUBI[/]",
            border_style="bright_red",
            width=60,
            padding=(1, 2),
        )

        console.print(Align.center(titulo))

        console.print()

        # =========================
        # MENU
        # =========================

        console.print("[bold bright_red]01[/]  " "[bold white]Bloquear computador[/]")

        console.print("[bold bright_red]02[/]  " "[bold white]Reiniciar computador[/]")

        console.print("[bold bright_red]03[/]  " "[bold white]Desligar computador[/]")

        console.print("[bold bright_red]04[/]  " "[bold white]Agendar desligamento[/]")

        console.print("[bold bright_red]05[/]  " "[bold white]Cancelar desligamento[/]")

        console.print()

        console.print("[dim]00  Voltar ao PyBoot[/]")

        console.print()

        # =========================
        # ESCOLHER OPÇÃO
        # =========================

        opcao = Prompt.ask("[bold bright_red]SISTEMA ❯[/]").strip()

        # =========================
        # EXECUTAR
        # =========================

        if opcao in ["1", "01"]:

            bloquear_computador()

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")

        elif opcao in ["2", "02"]:

            reiniciar_computador()

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")

        elif opcao in ["3", "03"]:

            desligar_computador()

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")

        elif opcao in ["4", "04"]:

            agendar_desligamento()

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")

        elif opcao in ["5", "05"]:

            cancelar_desligamento()

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")

        elif opcao in ["0", "00"]:

            break

        else:

            console.print()
            console.print("[bold red]✕ Opção inválida.[/]")

            Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")
