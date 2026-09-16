from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align


console = Console()


def pedir_opcao():
    console.print()

    mensagem = Panel(
        "[bold white]Escolha uma ferramenta para continuar[/]",
        border_style="bright_blue",
        width=50,
        padding=(0, 2),
    )

    console.print(Align.center(mensagem))

    console.print()

    opcao = Prompt.ask(
        "[bold bright_cyan]PYBOOT ❯[/]"
    )

    return opcao.strip()