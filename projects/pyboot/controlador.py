from rich.console import Console
from rich.prompt import Prompt

from functions.bronze.pesquisar_google import pesquisar_google
from functions.bronze.abrir_programa import abrir_programa

from functions.prata.pesquisar_youtube import pesquisar_youtube
from functions.prata.preparar_mensagem import preparar_mensagem

from functions.ouro.tocar_musica import tocar_musica
from functions.ouro.encontrar_arquivo import encontrar_arquivo
from functions.ouro.organizar_downloads import organizar_downloads

from functions.diamante.fechar_janelas import fechar_janelas
from functions.diamante.limpar_temporarios import limpar_temporarios

from functions.rubi.central_sistema import central_sistema
from functions.rubi.automacao_personalizada import automacao_personalizada

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
    # PRATA
    # =========================

    elif opcao in ["3", "03"]:

        pesquisar_youtube()

        voltar_menu()

        return True

    elif opcao in ["4", "04"]:

        preparar_mensagem()

        voltar_menu()

        return True

    # =========================
    # OURO
    # =========================

    elif opcao in ["5", "05"]:

        tocar_musica()

        voltar_menu()

        return True

    elif opcao in ["6", "06"]:

        encontrar_arquivo()

        voltar_menu()

        return True

    elif opcao in ["7", "07"]:

        organizar_downloads()

        voltar_menu()

        return True

    # =========================
    # DIAMANTE
    # =========================

    elif opcao in ["8", "08"]:

        fechar_janelas()

        voltar_menu()

        return True

    elif opcao in ["9", "09"]:
        limpar_temporarios()
        voltar_menu()
        return True

    # =========================
    # RUBI
    # =========================

    elif opcao in ["10"]:
        central_sistema()
        return True

    elif opcao == "11":
        automacao_personalizada()
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
