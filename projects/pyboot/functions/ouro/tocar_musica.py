import time
import pyautogui

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align


console = Console()


# =========================
# COORDENADAS
# =========================

POSICAO_MUSICA = (537, 214)


def tocar_musica():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]TOCAR MÚSICA[/]\n"
        "[dim]Digite a música que deseja ouvir.[/]",
        title="[bold #FFD700]◆ OURO[/]",
        border_style="#FFD700",
        width=60,
        padding=(1, 2),
    )

    console.print(
        Align.center(titulo)
    )

    console.print()

    # =========================
    # RECEBER MÚSICA
    # =========================

    musica = Prompt.ask(
        "[bold bright_cyan]Música ❯[/]"
    ).strip()

    if not musica:

        console.print(
            "\n[bold red]✕ Digite o nome de uma música.[/]"
        )

        return

    # =========================
    # ABRIR REPRODUTOR
    # =========================

    console.print()

    console.print(
        "[bright_cyan]●[/] Abrindo Reprodutor Multimídia..."
    )

    # Abre o menu Iniciar
    pyautogui.press("win")

    time.sleep(0.8)

    # Pesquisa o programa
    pyautogui.write(
        "Reprodutor Multimidia",
        interval=0.04
    )

    time.sleep(0.8)

    # Abre o programa
    pyautogui.press("enter")

    time.sleep(2)

    # =========================
    # PESQUISAR MÚSICA
    # =========================

    console.print(
        f"[bright_cyan]●[/] Procurando "
        f'[bold white]"{musica}"[/]...'
    )

    # Atalho de pesquisa do Reprodutor
    pyautogui.hotkey(
        "ctrl",
        "e"
    )

    time.sleep(0.5)

    # Limpa uma pesquisa anterior
    pyautogui.hotkey(
        "ctrl",
        "a"
    )

    # Digita a música
    pyautogui.write(
        musica,
        interval=0.05
    )

    pyautogui.press("enter")

    # Espera os resultados aparecerem
    time.sleep(1.5)

    # =========================
    # REPRODUZIR
    # =========================

    pyautogui.doubleClick(
        *POSICAO_MUSICA,
        interval=0.15
    )

    time.sleep(1)

    # =========================
    # FINALIZAR
    # =========================

    console.print()

    console.print(
        "[bright_green]▶[/] "
        f'[bold white]Reproduzindo "{musica}"[/]'
    )