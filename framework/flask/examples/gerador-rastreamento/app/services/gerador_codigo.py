import secrets
import string
import time

def gerar_codigo(categoria_produto, tipo_entrega):
    prefixo_categoria = {
    "eletronicos": "EL",
    "roupas": "RP",
    "moveis": "MV",
    "livros": "LV",
    "outros": "OT"
}

    prefixo_entrega = {
        "normal": "NM",
        "expressa": "EX",
        "economica": "EC"
    }

    categoria = prefixo_categoria[categoria_produto]
    entrega = prefixo_entrega[tipo_entrega]

    
    milisegundos = str(int(time.time() * 1000))[-8:]  # Obtém os últimos 8 dígitos dos milissegundos

    separadores = "-_."
    caracteres_especial = secrets.choice(separadores)
    caracteres_especial2 = secrets.choice(separadores)
    caracteres_especial3 = secrets.choice(separadores)

    caracteres = string.ascii_uppercase + string.digits
    codigo = "".join(secrets.choice(caracteres) for _ in range(10))

    return f"BR-{categoria}{caracteres_especial}{entrega}{caracteres_especial2}{codigo}{caracteres_especial3}{milisegundos}-LRA"