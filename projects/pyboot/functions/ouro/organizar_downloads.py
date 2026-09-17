from pathlib import Path
import shutil

from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.align import Align


console = Console()


def organizar_downloads():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]ORGANIZAR DOWNLOADS[/]\n"
        "[dim]Organize automaticamente seus arquivos por categoria.[/]",
        title="[bold #FFD700]◆ OURO[/]",
        border_style="#FFD700",
        width=65,
        padding=(1, 2),
    )

    console.print(
        Align.center(titulo)
    )

    console.print()

    # =========================
    # PASTA DOWNLOADS
    # =========================

    pasta_downloads = Path.home() / "Downloads"

    if not pasta_downloads.exists():

        console.print(
            "[bold red]✕ Pasta Downloads não encontrada.[/]"
        )

        return

    # =========================
    # CATEGORIAS
    # =========================

    categorias = {

        "Imagens": [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp"
        ],

        "Documentos": [
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx"
        ],

        "Videos": [
            ".mp4",
            ".mkv",
            ".avi",
            ".mov"
        ],

        "Musicas": [
            ".mp3",
            ".wav",
            ".flac"
        ],

        "Compactados": [
            ".zip",
            ".rar",
            ".7z"
        ],

        "Programas": [
            ".exe",
            ".msi"
        ],
    }

    # =========================
    # CONFIRMAÇÃO
    # =========================

    console.print(
        "[yellow]⚠ Os arquivos da pasta Downloads "
        "serão movidos para pastas por categoria.[/]"
    )

    console.print()

    confirmar = Confirm.ask(
        "[bold white]Deseja continuar?[/]"
    )

    if not confirmar:

        console.print()

        console.print(
            "[dim]Organização cancelada.[/]"
        )

        return

    # =========================
    # ORGANIZAR
    # =========================

    total_movidos = 0

    console.print()

    for arquivo in pasta_downloads.iterdir():

        if not arquivo.is_file():
            continue

        extensao = arquivo.suffix.lower()

        for categoria, extensoes in categorias.items():

            if extensao in extensoes:

                destino = pasta_downloads / categoria

                destino.mkdir(
                    exist_ok=True
                )

                arquivo_destino = destino / arquivo.name

                # Evita substituir um arquivo existente
                if arquivo_destino.exists():

                    console.print(
                        f"[yellow]●[/] {arquivo.name} "
                        "[dim]já existe no destino.[/]"
                    )

                    break

                shutil.move(
                    str(arquivo),
                    str(arquivo_destino)
                )

                total_movidos += 1

                console.print(
                    f"[bright_green]✓[/] "
                    f"{arquivo.name} "
                    f"[dim]→[/] "
                    f"[bold]{categoria}[/]"
                )

                break

    # =========================
    # RESULTADO
    # =========================

    console.print()

    if total_movidos == 0:

        console.print(
            "[yellow]Nenhum arquivo precisou ser organizado.[/]"
        )

    else:

        console.print(
            f"[bold bright_green]✓ Organização concluída![/] "
            f"[white]{total_movidos} arquivo(s) movido(s).[/]"
        )