from rich import print

# Tupla contendo a senha correta
senhas_validas = ("123456", "admin123", "python2024")

# Variável para controlar tentativas
tentativas = 3

# Loop para permitir múltiplas tentativas
while tentativas > 0:
    # Solicita ao usuário que digite a senha
    senha_digitada = input("Digite sua senha: ")
    
    # Validação 1: Verifica se o campo está vazio
    if not senha_digitada:
        print("[red]✗ Senha não pode estar vazia![/red]")
        continue
    
    # Validação 2: Verifica o comprimento mínimo
    if len(senha_digitada) < 6:
        print("[red]✗ Senha deve ter no mínimo 6 caracteres![/red]")
        continue
    
    # Validação 3: Verifica se contém espaços
    if " " in senha_digitada:
        print("[red]✗ Senha não pode conter espaços![/red]")
        continue
    
    # Validação 4: Verifica se a senha está na tupla
    if senha_digitada in senhas_validas:
        print("[green]✓ Acesso concedido! Bem-vindo![/green]")
        break
    else:
        tentativas -= 1
        
        if tentativas > 0:
            print(f"[red]✗ Senha incorreta! Você possui {tentativas} tentativa(s) restante(s).[/red]")
        else:
            print("[red]✗ Acesso negado! Limite de tentativas excedido.[/red]")