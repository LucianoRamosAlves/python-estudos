from rich.console import Console

c = Console()


c.rule("Imojin :sushi:", style="bold red", align="center")
c.print("Olá, mundo! a hora :snail: é :clock1: 12:00", style=" blue on white", justify="right", emoji=True)
c.print("Eu gosto de :pizza: e :sushi:!", style="red on white reverse", justify="center", emoji=True, end="\n\n")