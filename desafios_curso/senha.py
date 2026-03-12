import tkinter as tk

# ==============================
# CONFIGURAÇÃO DA JANELA
# ==============================
janela = tk.Tk()
janela.title("Sistema Seguro")
janela.geometry("400x250")
janela.configure(bg="#1e1e1e")

# ==============================
# FUNÇÃO DE ANIMAÇÃO (NÃO MEXER)
# ==============================
def tremer():
    x = janela.winfo_x()
    y = janela.winfo_y()

    for i in range(10):
        janela.geometry(f"+{x+5}+{y}")
        janela.update()
        janela.geometry(f"+{x-5}+{y}")
        janela.update()

    janela.geometry(f"+{x}+{y}")

# ==============================
# FUNÇÕES VISUAIS (NÃO MEXER)
# ==============================
def mostrar_erro():
    mensagem.config(text="❌ Senha incorreta!", fg="red")
    tremer()

def mostrar_erro_space():
    mensagem.config(text="❌ Senha incorreta!, adcione letras", fg="#544566")
    tremer()

def mostrar_sucesso():
    mensagem.config(text="✅ Acesso liberado!", fg="lime")

# ==============================
# ===== SUA ÁREA DE LÓGICA =====
# ==============================
def verificar():
    senha_digitada = campo.get()

    # 👇 TREINE SEUS IF AQUI

    if senha_digitada == "1234":
        mostrar_sucesso()
    elif senha_digitada.isspace():
        mostrar_erro_space()  
    else:
        mostrar_erro()

# ==============================
# INTERFACE PRONTA (NÃO MEXER)
# ==============================

titulo = tk.Label(
    janela,
    text="PAINEL DE ACESSO",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
)
titulo.pack(pady=20)

campo = tk.Entry(
    janela,
    font=("Arial", 14),
    show="*",
    justify="center"
)
campo.pack(pady=10)

botao = tk.Button(
    janela,
    text="ENTRAR",
    font=("Arial", 12, "bold"),
    bg="#333",
    fg="white",
    command=verificar
)
botao.pack(pady=10)

mensagem = tk.Label(
    janela,
    text="",
    font=("Arial", 12),
    bg="#1e1e1e"
)
mensagem.pack()

janela.mainloop()