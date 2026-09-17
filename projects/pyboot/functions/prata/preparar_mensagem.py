import os
import time
import pyautogui

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

console = Console()


# =========================
# COORDENADAS DO WHATSAPP
# =========================

POSICAO_PESQUISA = (289, 154)
POSICAO_CONTATO = (182, 355)
POSICAO_MENSAGEM = (906, 1092)


def preparar_mensagem():

    console.clear()

    # =========================
    # TÍTULO
    # =========================

    titulo = Panel(
        "[bold white]PREPARAR MENSAGEM[/]\n"
        "[dim]Escolha o contato e escreva sua mensagem.[/]",
        title="[bold #C0C0C0]◆ PRATA[/]",
        border_style="#C0C0C0",
        width=60,
        padding=(1, 2),
    )

    console.print(Align.center(titulo))

    console.print()

    # =========================
    # RECEBER DADOS
    # =========================

    console.print("[dim]Digite 0 para voltar ao PyBoot[/]")

    console.print()

    contato = Prompt.ask("[bold bright_cyan]Contato ❯[/]").strip()

    # =========================
    # VOLTAR
    # =========================

    if contato == "0":
        return

    # =========================
    # VALIDAR CONTATO
    # =========================

    if not contato:

        console.print("\n[bold red]✕ Digite o nome do contato.[/]")

        return

    mensagem = Prompt.ask("[bold bright_cyan]Mensagem ❯[/]").strip()

    # =========================
    # VOLTAR
    # =========================

    if mensagem == "0":
        return

    # =========================
    # VALIDAR MENSAGEM
    # =========================

    if not mensagem:

        console.print("\n[bold red]✕ Digite uma mensagem.[/]")

        return
    # =========================
    # ABRIR WHATSAPP
    # =========================

    console.print()
    console.print("[bright_cyan]●[/] Abrindo WhatsApp...")

    os.startfile("whatsapp:")

    time.sleep(2)

    # =========================
    # MAXIMIZAR JANELA
    # =========================

    pyautogui.hotkey("win", "up")

    time.sleep(1)

    # =========================
    # PESQUISAR CONTATO
    # =========================

    console.print(f"[bright_cyan]●[/] Procurando " f"[bold white]{contato}[/]...")

    pyautogui.click(*POSICAO_PESQUISA)

    time.sleep(2)

    pyautogui.hotkey("ctrl", "a")

    pyautogui.write(contato, interval=0.03)

    # Espera aparecer o resultado
    time.sleep(0.8)

    # =========================
    # ABRIR CONTATO
    # =========================

    pyautogui.click(*POSICAO_CONTATO)

    time.sleep(0.6)

    # =========================
    # ESCREVER MENSAGEM
    # =========================

    pyautogui.click(*POSICAO_MENSAGEM)

    pyautogui.write(mensagem, interval=0.08)

    # Pequena pausa antes de enviar
    time.sleep(1.5)

    # =========================
    # ENVIAR
    # =========================

    pyautogui.press("enter")

    console.print()

    console.print("[bright_green]✓[/] " "[bold white]Mensagem enviada com sucesso![/]")
