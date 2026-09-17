import tempfile
import shutil
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.align import Align


console = Console()


def formatar_tamanho(bytes_total):

    mb = bytes_total / (1024 * 1024)

    if mb < 1024:
        return f"{mb:.2f} MB"

    gb = mb / 1024

    return f"{gb:.2f} GB"


def calcular_tamanho(item):

    tamanho = 0

    try:

        # =========================
        # SE FOR ARQUIVO
        # =========================

        if item.is_file():

            tamanho = item.stat().st_size

        # =========================
        # SE FOR PASTA
        # =========================

        elif item.is_dir():

            for arquivo in item.rglob("*"):

                try:

                    if arquivo.is_file():
                        tamanho += arquivo.stat().st_size

                except (PermissionError, OSError):
                    continue

    except (PermissionError, OSError):

        pass

    return tamanho


def limpar_temporarios():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]LIMPAR TEMPORÁRIOS[/]\n"
        "[dim]Remova arquivos temporários que não estão em uso.[/]",
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
    # LOCALIZAR PASTA TEMP
    # =========================

    pasta_temp = Path(
        tempfile.gettempdir()
    )

    console.print(
        "[bright_cyan]●[/] Analisando arquivos temporários..."
    )

    console.print()

    # =========================
    # ANALISAR TEMPORÁRIOS
    # =========================

    itens = []
    tamanho_total = 0

    try:

        for item in pasta_temp.iterdir():

            itens.append(item)

            tamanho_total += calcular_tamanho(item)

    except (PermissionError, OSError):

        console.print(
            "[bold red]✕ Não foi possível acessar "
            "a pasta de temporários.[/]"
        )

        return

    # =========================
    # NENHUM ITEM
    # =========================

    if not itens:

        console.print(
            "[yellow]Nenhum arquivo temporário encontrado.[/]"
        )

        return

    # =========================
    # MOSTRAR ANÁLISE
    # =========================

    console.print(
        f"[white]Itens encontrados:[/] "
        f"[bold]{len(itens)}[/]"
    )

    console.print(
        f"[white]Espaço ocupado:[/] "
        f"[bold]{formatar_tamanho(tamanho_total)}[/]"
    )

    console.print()

    console.print(
        "[yellow]⚠ Arquivos que estiverem em uso "
        "serão ignorados.[/]"
    )

    # =========================
    # CONFIRMAÇÃO
    # =========================

    console.print()

    confirmar = Confirm.ask(
        "[bold white]Deseja realizar a limpeza?[/]"
    )

    if not confirmar:

        console.print()

        console.print(
            "[dim]Limpeza cancelada.[/]"
        )

        return

    # =========================
    # LIMPAR TEMPORÁRIOS
    # =========================

    console.print()

    console.print(
        "[bright_cyan]●[/] Limpando arquivos temporários..."
    )

    console.print()

    removidos = 0
    ignorados = 0
    espaco_liberado = 0

    for item in itens:

        try:

            tamanho_item = calcular_tamanho(item)

            # =========================
            # REMOVER ARQUIVO
            # =========================

            if item.is_file():

                item.unlink()

            # =========================
            # REMOVER PASTA
            # =========================

            elif item.is_dir():

                shutil.rmtree(item)

            else:

                continue

            removidos += 1
            espaco_liberado += tamanho_item

        except (PermissionError, OSError):

            ignorados += 1

    # =========================
    # RESULTADO
    # =========================

    console.print(
        "[bold bright_green]✓ Limpeza concluída![/]"
    )

    console.print()

    console.print(
        f"[bright_green]✓[/] "
        f"[white]{removidos} item(ns) removido(s)[/]"
    )

    if ignorados:

        console.print(
            f"[yellow]⚠[/] "
            f"[white]{ignorados} item(ns) em uso "
            f"ou protegidos[/]"
        )

    console.print(
        f"[bright_green]✓[/] "
        f"[white]Espaço liberado: "
        f"[bold]{formatar_tamanho(espaco_liberado)}[/][/]"
    )