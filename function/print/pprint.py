# Importando pprint
from pprint import pprint

# Estrutura bem grande e bagunçada (tipo resposta de API)
dados = {
    "usuario": {
        "id": 1,
        "nome": "Luciano",
        "emails": ["luciano@gmail.com", "lucas@outlook.com"],
        "endereco": {
            "cidade": "Coroatá",
            "estado": "MA",
            "cep": "65415-000"
        }
    },
    "posts": [
        {
            "id": 101,
            "titulo": "Aprendendo Python",
            "comentarios": [
                {"usuario": "Ana", "texto": "Muito bom!"},
                {"usuario": "Carlos", "texto": "Top demais!"}
            ]
        },
        {
            "id": 102,
            "titulo": "Flask é massa",
            "comentarios": [
                {"usuario": "João", "texto": "Gostei!"},
                {"usuario": "Maria", "texto": "Explica mais!"}
            ]
        }
    ]
}

# ---------------------------
# PRINT NORMAL (bagunçado)
# ---------------------------
print("PRINT NORMAL:\n")
print(dados)

print("\n" + "="*60 + "\n")

# ---------------------------
# PPRINT (organizado)
# ---------------------------
print("PPRINT:\n")
pprint(dados)