from rich.console import Console
from rich.prompt import Prompt

from functions.bronze.pesquisar_google import pesquisar_google
from functions.bronze.abrir_programa import abrir_programa

console = Console()


def voltar_menu():
    console.print()

    Prompt.ask("[dim]Pressione ENTER para voltar ao PyBoot[/]", default="")


def executar_opcao(opcao):

    # =========================
    # BRONZE
    # =========================

    if opcao in ["1", "01"]:

        pesquisar_google()

        voltar_menu()

        return True

    elif opcao in ["2", "02"]:

        abrir_programa()

        voltar_menu()

        return True

    # =========================
    # SAIR
    # =========================

    elif opcao == "0":

        console.clear()

        console.print("\n[bold bright_cyan]" "PyBoot finalizado." "[/]\n")

        return False

    # =========================
    # OPÇÃO INVÁLIDA
    # =========================

    else:

        console.print()

        console.print("[bold red]✕ Opção inválida.[/]")

        voltar_menu()

        return True
