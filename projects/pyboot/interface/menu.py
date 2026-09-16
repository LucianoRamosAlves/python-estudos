from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text


console = Console()


# =========================
# CORES DOS NÍVEIS
# =========================

COR_BRONZE = "#CD7F32"
COR_PRATA = "#C0C0C0"
COR_OURO = "#FFD700"
COR_DIAMANTE = "bright_cyan"
COR_RUBI = "bright_red"


def criar_conteudo(opcoes, cor):
    conteudo = Text()

    for indice, (numero, nome) in enumerate(opcoes):
        conteudo.append(
            f"{numero:02}  ",
            style=f"bold {cor}"
        )

        conteudo.append(
            nome,
            style="bold bright_white"
        )

        # Não adiciona linha vazia depois da última opção
        if indice < len(opcoes) - 1:
            conteudo.append("\n")

    return conteudo


def criar_painel(titulo, opcoes, cor, largura=43):
    return Panel(
        criar_conteudo(opcoes, cor),

        title=f"[bold {cor}]◆ {titulo}[/]",
        title_align="left",

        border_style=cor,

        width=largura,

        # Sem altura fixa:
        # o painel cresce apenas o necessário
        padding=(0, 2),
    )


def mostrar_menu():

    # =========================
    # BRONZE
    # =========================

    bronze = criar_painel(
        "BRONZE",
        [
            (1, "Central de Pesquisa"),
            (2, "Abrir Programa"),
        ],
        COR_BRONZE
    )

    # =========================
    # PRATA
    # =========================

    prata = criar_painel(
        "PRATA",
        [
            (3, "Pesquisar no YouTube"),
            (4, "Preparar Mensagem"),
        ],
        COR_PRATA
    )

    # =========================
    # OURO
    # =========================

    ouro = criar_painel(
        "OURO",
        [
            (5, "Tocar Música"),
            (6, "Encontrar Arquivo"),
            (7, "Organizar Downloads"),
        ],
        COR_OURO
    )

    # =========================
    # DIAMANTE
    # =========================

    diamante = criar_painel(
        "DIAMANTE",
        [
            (8, "Fechar Janelas"),
            (9, "Limpar Temporários"),
        ],
        COR_DIAMANTE
    )

    # =========================
    # RUBI
    # =========================

    rubi = criar_painel(
        "RUBI",
        [
            (10, "Central do Sistema"),
            (11, "Automação Personalizada"),
        ],
        COR_RUBI,
        largura=50
    )

    # =========================
    # GRID 2 x 2
    # =========================

    grade = Table.grid(
        padding=(0, 1)
    )

    grade.add_column(width=43)
    grade.add_column(width=43)

    grade.add_row(bronze, prata)
    grade.add_row(ouro, diamante)

    console.print(
        Align.center(grade)
    )

    # Espaço pequeno antes do Rubi
    console.print()

    console.print(
        Align.center(rubi)
    )

    console.print()

    # =========================
    # STATUS
    # =========================

    status = Text()

    status.append(
        "● ",
        style="bright_green"
    )

    status.append(
        "ONLINE",
        style="bold bright_green"
    )

    status.append(
        "  │  ",
        style="dim"
    )

    status.append(
        "11 ferramentas disponíveis",
        style="bright_white"
    )

    console.print(
        Align.center(status)
    )

    console.print()