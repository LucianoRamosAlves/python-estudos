from datetime import datetime
data = datetime.now()
caixa = 500

def divida(valor):
    global caixa
    if valor <= caixa:
        caixa -= valor
    else:
        return print("saldo no caixa insuficiente.")
    return caixa

