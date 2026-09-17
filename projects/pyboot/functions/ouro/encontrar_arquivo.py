from pathlib import Path
import subprocess

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()


def encontrar_arquivo():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]ENCONTRAR ARQUIVO[/]\n"
        "[dim]Procure arquivos pelo nome no seu computador.[/]",
        title="[bold #FFD700]◆ OURO[/]",
        border_style="#FFD700",
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

    nome = Prompt.ask("[bold bright_cyan]Arquivo ❯[/]").strip()

    # =========================
    # VOLTAR
    # =========================

    if nome == "0":
        return

    # =========================
    # VALIDAR
    # =========================

    if not nome:

        console.print("\n[bold red]✕ Digite o nome do arquivo.[/]")

        return

    console.print()

    console.print(f"[bright_cyan]●[/] Procurando " f'[bold white]"{nome}"[/]...')

    # =========================
    # PASTAS PARA PESQUISAR
    # =========================

    usuario = Path.home()

    pastas = [
        usuario / "Downloads",
        usuario / "Documents",
        usuario / "Desktop",
        usuario / "Pictures",
        usuario / "Videos",
        usuario / "Music",
    ]

    # =========================
    # PROCURAR ARQUIVO
    # =========================

    arquivo_encontrado = None

    for pasta in pastas:

        if not pasta.exists():
            continue

        for arquivo in pasta.rglob("*"):

            if arquivo.is_file():

                if nome.lower() in arquivo.name.lower():

                    arquivo_encontrado = arquivo
                    break

        if arquivo_encontrado:
            break

    # =========================
    # NÃO ENCONTROU
    # =========================

    if not arquivo_encontrado:

        console.print()

        console.print("[bold red]✕ Arquivo não encontrado.[/]")

        return

    # =========================
    # ARQUIVO ENCONTRADO
    # =========================

    console.print()

    console.print("[bright_green]✓[/] " "[bold white]Arquivo encontrado![/]")

    console.print()

    console.print(f"[dim]{arquivo_encontrado}[/]")

    # =========================
    # ABRIR LOCALIZAÇÃO
    # =========================

    console.print()

    console.print("[bright_cyan]●[/] Abrindo localização...")

    subprocess.Popen(["explorer", "/select,", str(arquivo_encontrado)])
