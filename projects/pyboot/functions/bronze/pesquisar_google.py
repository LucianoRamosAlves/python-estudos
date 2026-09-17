import webbrowser
from urllib.parse import quote_plus

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()


def pesquisar_google():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]PESQUISAR NO GOOGLE[/]\n"
        "[dim]Digite o que deseja encontrar na internet.[/]",
        title="[bold #CD7F32]◆ BRONZE[/]",
        border_style="#CD7F32",
        width=60,
        padding=(1, 2),
    )

    console.print(Align.center(titulo))

    console.print()

    # =========================
    # RECEBER PESQUISA
    # =========================

    console.print("[dim]Digite 0 para voltar ao PyBoot[/]")

    console.print()

    pesquisa = Prompt.ask("[bold bright_cyan]Pesquisa ❯[/]").strip()

    # =========================
    # VOLTAR
    # =========================

    if pesquisa == "0":
        return

    # =========================
    # VALIDAR
    # =========================

    if not pesquisa:

        console.print()

        console.print("[bold red]✕ Digite algo para pesquisar.[/]")

        return

    # =========================
    # PREPARAR PESQUISA
    # =========================

    pesquisa_url = quote_plus(pesquisa)

    url = "https://www.google.com/search" f"?q={pesquisa_url}"

    # =========================
    # ABRIR GOOGLE
    # =========================

    console.print()

    console.print(
        f"[bright_green]✓[/] Pesquisando por " f'[bold white]"{pesquisa}"[/]...'
    )

    webbrowser.open(url)
