import subprocess

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()


def abrir_programa():
    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]ABRIR PROGRAMA[/]\n"
        "[dim]Digite o nome do programa que deseja abrir.[/]",
        title="[bold #CD7F32]◆ BRONZE[/]",
        border_style="#CD7F32",
        width=60,
        padding=(1, 2),
    )

    console.print(Align.center(titulo))

    console.print()

    # =========================
    # PROGRAMAS DISPONÍVEIS
    # =========================

    programas = {
        "bloco de notas": "notepad",
        "notepad": "notepad",
        "calculadora": "calc",
        "calc": "calc",
        "paint": "mspaint",
        "explorador": "explorer",
        "arquivos": "explorer",
        "cmd": "cmd",
        "powershell": "powershell",
        "hp": r"C:\Program Files (x86)\HP\Digital Imaging\bin\Hpqdirec.exe",
        "send": r"C:\Users\lramo\AppData\Local\Programs\LocalSend\localsend_app.exe",
    }

    # =========================
    # RECEBER PROGRAMA
    # =========================

    console.print("[dim]Digite 0 para voltar ao PyBoot[/]")

    console.print()

    nome = Prompt.ask("[bold bright_cyan]Programa ❯[/]")

    nome = nome.strip().lower()

    # =========================
    # VOLTAR
    # =========================

    if nome == "0":
        return

    # =========================
    # VALIDAR
    # =========================

    if not nome:

        console.print()

        console.print("[bold red]✕ Digite o nome de um programa.[/]")

        return
    # =========================
    # PROCURAR PROGRAMA
    # =========================

    programa = programas.get(nome)

    if not programa:
        console.print()

        console.print(f'[bold red]✕ Programa "{nome}" ' f"não encontrado.[/]")

        console.print()

        console.print(
            "[dim]Tente, por exemplo: "
            "calculadora, paint, bloco de notas ou explorador.[/]"
        )

        return

    # =========================
    # ABRIR PROGRAMA
    # =========================

    try:
        subprocess.Popen([programa])

        console.print()

        console.print(f"[bright_green]✓[/] Abrindo " f'[bold white]"{nome}"[/]...')

    except Exception:
        console.print()

        console.print("[bold red]✕ Não foi possível abrir o programa.[/]")
