from time import sleep
from rich.console import Console

console = Console()

with console.status("[bold blue]Carregando...", spinner="aesthetic", spinner_style="bold blue") as status:
    sleep(2)