import pyautogui


# Pega todas as janelas abertas
janelas = pyautogui.getAllWindows()


# Mostra as janelas encontradas
for janela in janelas:

    if janela.title:

        print(janela.title)