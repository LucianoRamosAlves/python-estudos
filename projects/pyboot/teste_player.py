import time
import pyautogui


# Abre o menu Iniciar
pyautogui.press("win")

time.sleep(1)

# Pesquisa o aplicativo
pyautogui.write(
    "Reprodutor Multimidia",
    interval=0.05
)

time.sleep(1)

# Abre o aplicativo encontrado
pyautogui.press("enter")