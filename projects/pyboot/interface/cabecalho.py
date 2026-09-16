from pyfiglet import Figlet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.rule import Rule


console = Console()


def criar_logo_colorida(logo):
    cores = [
        "bright_cyan",
        "cyan",
        "bright_blue",
        "bright_magenta",
        "magenta",
    ]

    texto = Text()

    for indice, linha in enumerate(logo.splitlines()):
        cor = cores[indice % len(cores)]

        texto.append(linha, style=f"bold {cor}")
        texto.append("\n")

    return texto


def mostrar_cabecalho():
    console.clear()

    # Fonte com aparência mais sólida/preenchida
    figlet = Figlet(font="big")

    logo = figlet.renderText("PyBoot")
    logo_colorida = criar_logo_colorida(logo)

    console.print(
        Align.center(logo_colorida)
    )

    console.print(
        Align.center(
            "[bold bright_cyan]AUTOMAÇÃO[/] "
            "[dim]•[/] "
            "[bold bright_magenta]PRODUTIVIDADE[/] "
            "[dim]•[/] "
            "[bold bright_green]ARQUIVOS[/] "
            "[dim]•[/] "
            "[bold bright_yellow]SISTEMA[/]"
        )
    )

    console.print()

    console.print(
        Rule(
            "[bold bright_cyan] PYBOOT SYSTEM [/]",
            style="bright_blue"
        )
    )

    console.print()