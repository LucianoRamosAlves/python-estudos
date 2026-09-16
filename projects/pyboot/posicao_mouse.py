import time
import pyautogui


print("Coloque o mouse sobre a barra de pesquisa do YouTube.")
print("Você tem 5 segundos...")


time.sleep(5)


posicao = pyautogui.position()


print()
print(f"Posição do mouse: {posicao}")