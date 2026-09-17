import os
import time
import webbrowser
import pyautogui

from urllib.parse import quote_plus
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.align import Align

console = Console()


# =========================
# PROGRAMAS DISPONÍVEIS
# =========================

PROGRAMAS = {
    "chrome": "chrome",
    "edge": "msedge",
    "calculadora": "calc",
    "bloco de notas": "notepad",
    "paint": "mspaint",
    "explorador": "explorer",
}


# =========================
# MOSTRAR MENU
# =========================


def mostrar_opcoes():

    console.print("[bold bright_red]01[/]  " "[bold white]Abrir programa[/]")

    console.print("[bold bright_red]02[/]  " "[bold white]Abrir site[/]")

    console.print("[bold bright_red]03[/]  " "[bold white]Pesquisar no Google[/]")

    console.print("[bold bright_red]04[/]  " "[bold white]Aguardar[/]")

    console.print("[bold bright_red]05[/]  " "[bold white]Abrir pasta[/]")

    console.print()

    console.print("[bold bright_green]06[/]  " "[bold white]Executar automação[/]")

    console.print("[dim]00  Cancelar[/]")


# =========================
# ADICIONAR PROGRAMA
# =========================


def adicionar_programa(rotina):

    console.print()

    console.print(
        "[dim]Exemplos: Chrome, Edge, Calculadora, "
        "Bloco de Notas, Paint, Explorador[/]"
    )

    console.print()

    programa = Prompt.ask("[bold bright_cyan]Programa ❯[/]").strip().lower()

    if programa not in PROGRAMAS:

        console.print()

        console.print("[bold red]✕ Programa não configurado.[/]")

        return

    rotina.append({"tipo": "programa", "nome": programa})

    console.print()

    console.print(
        f"[bright_green]✓[/] " f"[white]{programa.title()} adicionado à rotina.[/]"
    )


# =========================
# ADICIONAR SITE
# =========================


def adicionar_site(rotina):

    console.print()

    site = Prompt.ask("[bold bright_cyan]Site ❯[/]").strip()

    if not site:

        console.print("\n[bold red]✕ Digite um site.[/]")

        return

    if not site.startswith(("http://", "https://")):
        site = "https://" + site

    rotina.append({"tipo": "site", "valor": site})

    console.print()

    console.print("[bright_green]✓[/] " "[white]Site adicionado à rotina.[/]")


# =========================
# ADICIONAR PESQUISA
# =========================


def adicionar_pesquisa(rotina):

    console.print()

    pesquisa = Prompt.ask("[bold bright_cyan]Pesquisar ❯[/]").strip()

    if not pesquisa:

        console.print("\n[bold red]✕ Digite algo para pesquisar.[/]")

        return

    rotina.append({"tipo": "pesquisa", "valor": pesquisa})

    console.print()

    console.print("[bright_green]✓[/] " "[white]Pesquisa adicionada à rotina.[/]")


# =========================
# ADICIONAR ESPERA
# =========================


def adicionar_espera(rotina):

    console.print()

    segundos = Prompt.ask("[bold bright_cyan]Quantos segundos? ❯[/]").strip()

    if not segundos.isdigit():

        console.print()

        console.print("[bold red]✕ Digite apenas números.[/]")

        return

    segundos = int(segundos)

    rotina.append({"tipo": "espera", "valor": segundos})

    console.print()

    console.print(
        f"[bright_green]✓[/] " f"[white]Espera de {segundos} segundo(s) adicionada.[/]"
    )


# =========================
# ADICIONAR PASTA
# =========================


def adicionar_pasta(rotina):

    console.print()

    console.print(
        "[dim]Exemplos: Downloads, Documentos, " "Imagens, Vídeos, Músicas[/]"
    )

    console.print()

    pasta = Prompt.ask("[bold bright_cyan]Pasta ❯[/]").strip().lower()

    rotina.append({"tipo": "pasta", "nome": pasta})

    console.print()

    console.print(f"[bright_green]✓[/] " f"[white]Pasta adicionada à rotina.[/]")


# =========================
# MOSTRAR ROTINA
# =========================


def mostrar_rotina(rotina):

    console.print()

    console.print("[bold bright_red]♦ AUTOMAÇÃO CRIADA[/]")

    console.print()

    for numero, tarefa in enumerate(rotina, start=1):

        tipo = tarefa["tipo"]

        if tipo == "programa":

            descricao = f"Abrir {tarefa['nome'].title()}"

        elif tipo == "site":

            descricao = f"Abrir {tarefa['valor']}"

        elif tipo == "pesquisa":

            descricao = f'Pesquisar "{tarefa["valor"]}"'

        elif tipo == "espera":

            descricao = f'Aguardar {tarefa["valor"]} segundo(s)'

        elif tipo == "pasta":

            descricao = f'Abrir pasta {tarefa["nome"].title()}'

        console.print(f"[bright_red]{numero:02}[/]  " f"[white]{descricao}[/]")


# =========================
# EXECUTAR TAREFA
# =========================


def executar_tarefa(tarefa):

    tipo = tarefa["tipo"]

    # =========================
    # PROGRAMA
    # =========================

    if tipo == "programa":

        programa = PROGRAMAS[tarefa["nome"]]

        os.system(f"start {programa}")

    # =========================
    # SITE
    # =========================

    elif tipo == "site":

        webbrowser.open(tarefa["valor"])

    # =========================
    # PESQUISA
    # =========================

    elif tipo == "pesquisa":

        pesquisa = quote_plus(tarefa["valor"])

        url = "https://www.google.com/search" f"?q={pesquisa}"

        webbrowser.open(url)

    # =========================
    # ESPERA
    # =========================

    elif tipo == "espera":

        time.sleep(tarefa["valor"])

    # =========================
    # PASTA
    # =========================

    elif tipo == "pasta":

        pastas = {
            "downloads": "Downloads",
            "documentos": "Documents",
            "imagens": "Pictures",
            "videos": "Videos",
            "vídeos": "Videos",
            "musicas": "Music",
            "músicas": "Music",
        }

        nome = tarefa["nome"]

        if nome in pastas:

            caminho = os.path.join(os.path.expanduser("~"), pastas[nome])

            os.startfile(caminho)


# =========================
# EXECUTAR AUTOMAÇÃO
# =========================


def executar_automacao(rotina):

    console.clear()

    titulo = Panel(
        "[bold white]EXECUTANDO AUTOMAÇÃO[/]\n"
        "[dim]O PyBoot está executando sua rotina.[/]",
        title="[bold bright_red]◆ RUBI[/]",
        border_style="bright_red",
        width=65,
        padding=(1, 2),
    )

    console.print(Align.center(titulo))

    console.print()

    total = len(rotina)

    for numero, tarefa in enumerate(rotina, start=1):

        tipo = tarefa["tipo"]

        console.print(
            f"[bright_red][{numero}/{total}][/]"
            f" Executando "
            f"[bold white]{tipo}[/]..."
        )

        try:

            executar_tarefa(tarefa)

            console.print("[bright_green]      ✓ Concluído[/]")

        except Exception:

            console.print("[red]      ✕ Não foi possível executar[/]")

        time.sleep(0.5)

    console.print()

    console.print("[bold bright_green]" "✓ AUTOMAÇÃO CONCLUÍDA" "[/]")

    console.print()

    console.print(f"[white]{total} tarefa(s) processada(s).[/]")


# =========================
# AUTOMAÇÃO PERSONALIZADA
# =========================


def automacao_personalizada():

    rotina = []

    while True:

        console.clear()

        titulo = Panel(
            "[bold white]AUTOMAÇÃO PERSONALIZADA[/]\n"
            "[dim]Monte uma sequência de tarefas "
            "para o PyBoot executar.[/]",
            title="[bold bright_red]◆ RUBI[/]",
            border_style="bright_red",
            width=65,
            padding=(1, 2),
        )

        console.print(Align.center(titulo))

        console.print()

        # =========================
        # QUANTIDADE DE TAREFAS
        # =========================

        console.print(
            f"[bright_cyan]●[/] "
            f"[white]Tarefas adicionadas: "
            f"[bold]{len(rotina)}[/][/]"
        )

        console.print()

        mostrar_opcoes()

        console.print()

        opcao = Prompt.ask("[bold bright_red]AUTOMAÇÃO ❯[/]").strip()

        # =========================
        # OPÇÕES
        # =========================

        if opcao in ["1", "01"]:

            adicionar_programa(rotina)

        elif opcao in ["2", "02"]:

            adicionar_site(rotina)

        elif opcao in ["3", "03"]:

            adicionar_pesquisa(rotina)

        elif opcao in ["4", "04"]:

            adicionar_espera(rotina)

        elif opcao in ["5", "05"]:

            adicionar_pasta(rotina)

        elif opcao in ["6", "06"]:

            if not rotina:

                console.print()

                console.print("[yellow]Adicione pelo menos " "uma tarefa primeiro.[/]")

            else:

                mostrar_rotina(rotina)

                console.print()

                confirmar = Confirm.ask("[bold white]" "Executar esta automação?" "[/]")

                if confirmar:

                    executar_automacao(rotina)

                    Prompt.ask(
                        "\n[dim]Pressione ENTER " "para voltar ao PyBoot[/]", default=""
                    )

                    break

        elif opcao in ["0", "00"]:

            break

        else:

            console.print()

            console.print("[bold red]✕ Opção inválida.[/]")

        Prompt.ask("\n[dim]Pressione ENTER para continuar[/]", default="")
