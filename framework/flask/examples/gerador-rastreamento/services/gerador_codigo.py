import secrets
import string
import time



def gerar_codigo():
    milisegundos = str(int(time.time() * 1000))[-8:]  # Obtém os últimos 8 dígitos dos milissegundos

    separadores = "-_."
    caracteres_especial = secrets.choice(separadores)

    caracteres = string.ascii_uppercase + string.digits
    codigo = "".join(secrets.choice(caracteres) for _ in range(10))

    return f"BR-{codigo}{caracteres_especial}{milisegundos}-LRA"

codigo = gerar_codigo()
print(codigo)