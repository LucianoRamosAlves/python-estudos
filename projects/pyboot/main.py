from interface.cabecalho import mostrar_cabecalho
from interface.menu import mostrar_menu
from interface.entrada import pedir_opcao

from controlador import executar_opcao


def iniciar():

    while True:

        # =========================
        # MOSTRAR PYBOOT
        # =========================

        mostrar_cabecalho()
        mostrar_menu()

        # =========================
        # RECEBER OPÇÃO
        # =========================

        opcao = pedir_opcao()

        # =========================
        # EXECUTAR OPÇÃO
        # =========================

        continuar = executar_opcao(opcao)

        if not continuar:
            break


if __name__ == "__main__":
    iniciar()