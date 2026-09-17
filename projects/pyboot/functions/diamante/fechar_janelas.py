import time
import pyautogui

from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.align import Align


console = Console()


# =========================
# PROGRAMAS PERMITIDOS
# =========================

PROGRAMAS_PARA_FECHAR = [
    "Google Chrome",
    "Microsoft Edge",
    "Mozilla Firefox",
    "WhatsApp",
    "Discord",
    "Spotify",
    "Reprodutor Multimídia",
    "Media Player",
    "Calculadora",
    "Bloco de Notas",
    "Notepad",
    "Paint",
    "Explorador de Arquivos",
    "GitHub Desktop",
]


def fechar_janelas():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]FECHAR JANELAS[/]\n"
        "[dim]Feche seus principais aplicativos de uma só vez.[/]",
        title="[bold bright_cyan]◆ DIAMANTE[/]",
        border_style="bright_cyan",
        width=65,
        padding=(1, 2),
    )

    console.print(
        Align.center(titulo)
    )

    console.print()

    # =========================
    # PEGAR JANELAS ABERTAS
    # =========================

    todas_janelas = pyautogui.getAllWindows()

    janelas_para_fechar = []

    # =========================
    # FILTRAR JANELAS
    # =========================

    for janela in todas_janelas:

        titulo_janela = janela.title.strip()

        if not titulo_janela:
            continue

        for programa in PROGRAMAS_PARA_FECHAR:

            if programa.lower() in titulo_janela.lower():

                janelas_para_fechar.append(janela)

                break

    # =========================
    # NENHUM PROGRAMA
    # =========================

    if not janelas_para_fechar:

        console.print(
            "[yellow]Nenhum dos programas configurados está aberto.[/]"
        )

        return

    # =========================
    # MOSTRAR O QUE SERÁ FECHADO
    # =========================

    console.print(
        "[bold white]Programas encontrados:[/]"
    )

    console.print()

    for janela in janelas_para_fechar:

        console.print(
            f"[bright_cyan]•[/] "
            f"[white]{janela.title}[/]"
        )

    console.print()

    console.print(
        f"[yellow]⚠ {len(janelas_para_fechar)} "
        f"janela(s) serão fechadas.[/]"
    )

    # =========================
    # CONFIRMAÇÃO
    # =========================

    console.print()

    confirmar = Confirm.ask(
        "[bold white]Deseja continuar?[/]"
    )

    if not confirmar:

        console.print()

        console.print(
            "[dim]Operação cancelada.[/]"
        )

        return

    # =========================
    # FECHAR JANELAS
    # =========================

    console.print()

    total_fechadas = 0
    total_erros = 0

    for janela in janelas_para_fechar:

        nome_janela = janela.title.strip()

        try:

            console.print(
                f"[bright_cyan]●[/] Fechando "
                f"[white]{nome_janela}[/]..."
            )

            janela.close()

            total_fechadas += 1

            time.sleep(0.3)

        except Exception:

            console.print(
                f"[red]✕[/] Não foi possível fechar "
                f"[white]{nome_janela}[/]"
            )

            total_erros += 1

    # =========================
    # RESULTADO
    # =========================

    console.print()

    console.print(
        f"[bright_green]✓[/] "
        f"[bold white]{total_fechadas} janela(s) fechada(s).[/]"
    )

    if total_erros:

        console.print(
            f"[yellow]⚠ {total_erros} janela(s) "
            f"não puderam ser fechadas.[/]"
        )