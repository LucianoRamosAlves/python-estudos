import pyautogui # servi para automitizar clicks...etc..
import time
import pandas as pd
import pyperclip


pyautogui.PAUSE = 0.5 # tempo entre comados do pyautogui..

pyautogui.press('win')
pyautogui.write('edge')
pyautogui.press('enter')

time.sleep(2)  

pyautogui.hotkey('win', 'up')  # Maximize the window

link = 'https://drive.google.com/drive/'
pyautogui.write(link)
pyautogui.press('enter')



time.sleep(4)
pyautogui.click(x=855, y=511)  # Click to focus the window

time.sleep(4)
pyautogui.click(x=872, y=379) 

time.sleep(4)
pyautogui.click(x=1783, y=408) 

time.sleep(4)
pyautogui.click(x=1465, y=519)  # Click on the email link   Relatório de vendas Olá,

print(pyautogui.position())

time.sleep(3)

# usando o pandas

caminho = r"C:\Users\lramo\Downloads\analise_vendas_python (1).xlsx" 
tabela = pd.read_excel(caminho)
print(tabela)


tabela["Total"] = tabela["Preço Unitário"] * tabela["Quantidade"]

qtd_intens = tabela["Quantidade"].count()
qtd_intes_vendidos = tabela["Quantidade"].sum()
fatura_total = tabela["Total"].sum()

print(fatura_total)
print(qtd_intens)
print(qtd_intes_vendidos)


pyautogui.hotkey('ctrl', 't')  # outra aba
time.sleep(2)

pyautogui.write('https://mail.google.com/mail/u/0/#inbox')
pyautogui.press('enter')
time.sleep(5)


pyautogui.click(x=102, y=226)  # click no botão escrever
time.sleep(3)

pyautogui.write("kilmatues93@gmail.com")  # substitua pelo seu email
pyautogui.press('tab')
pyautogui.press('tab')

pyperclip.copy("Relatório de vendas")  # título do email
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('tab')

texto_email = f"""Olá,
segue o relatório de vendas do mês.

Faturamneto total: R${fatura_total:,.2f}
Quantidade de itens vendidos: {qtd_intes_vendidos}
Quantidade de itens: {qtd_intens}


qualquer dúvida, estou à disposição.
 Atenciosamente, Luciano Ramos"""


pyperclip.copy(texto_email) # qualquer texto que queira escrever, pode ser copiado e colado usando o pyperclip
pyautogui.hotkey('ctrl', 'v')
time.sleep(3)


pyautogui.click(x=1158, y=1160)  # click no botão escrever
