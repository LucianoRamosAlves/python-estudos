import time
import webbrowser

import pyautogui

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()


def pesquisar_youtube():
    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]PESQUISAR NO YOUTUBE[/]\n"
        "[dim]Digite o conteúdo que deseja pesquisar.[/]",
        title="[bold #C0C0C0]◆ PRATA[/]",
        border_style="#C0C0C0",
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

    pesquisa = Prompt.ask("[bold bright_cyan]Pesquisar ❯[/]").strip()

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
    # ABRIR YOUTUBE
    # =========================

    console.print()

    console.print("[bright_cyan]●[/] Abrindo YouTube...")

    webbrowser.open("https://www.youtube.com")

    # Espera o site carregar
    time.sleep(2)

    # =========================
    # AUTOMATIZAR PESQUISA
    # =========================

    console.print("[bright_cyan]●[/] Pesquisando...")

    # Atalho do YouTube para focar
    # na barra de pesquisa
    pyautogui.click(787, 139)

    time.sleep(1)

    # Digita a pesquisa
    pyautogui.write(pesquisa, interval=0.02)

    # Pressiona ENTER
    pyautogui.press("enter")

    console.print()

    console.print(
        f"[bright_green]✓[/] Pesquisa " f'[bold white]"{pesquisa}"[/] realizada.'
    )
