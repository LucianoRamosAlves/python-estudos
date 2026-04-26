from rich import print as rich_print
from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text

t = Text("Olá, mundo! 😄", style="bold red", justify="center")

rich_print(Panel(
    "Olá, mundo!",
    title="Painel",
    subtitle="Subtítulo",
    style="bold red",
    expand=False
))

rich_print(Panel(
    Align.center(t),
    box=box.ASCII2,
    title="Painel",
    subtitle="Subtítulo",
    style="bold blue",
    expand=True,
    border_style="blue",
    
))