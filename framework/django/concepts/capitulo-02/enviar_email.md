# Django 6.1 — Configurando envio de e-mail com Gmail e `.env`

## Objetivo

Nesta etapa configuramos o Django para enviar e-mails usando o servidor SMTP do Gmail.

Também evitamos colocar informações sensíveis diretamente no `settings.py`, como:

- e-mail;
- senha de app;
- chaves privadas;
- outras credenciais.

Para isso, usamos um arquivo:

```text
.env
```

A estrutura final fica aproximadamente assim:

```text
CinePost
│
├── .env
├── .env.example
├── .gitignore
├── manage.py
│
├── config/
│   └── settings.py
│
├── filmes/
│
└── venv/
```

---

# 1. O que é o `.env`?

O `.env` é um arquivo usado para guardar informações que não queremos escrever diretamente no código.

Exemplo:

```env
CINEPOST_EMAIL_USER=seuemail@gmail.com
CINEPOST_EMAIL_PASSWORD=sua_senha_de_app
```

Assim, em vez de colocar no `settings.py`:

```python
"username": "meuemail@gmail.com",
"password": "minha_senha",
```

fazemos o Django buscar essas informações no ambiente.

Isso é muito mais seguro.

---

# 2. Por que não colocar senha no `settings.py`?

Nunca é uma boa ideia fazer:

```python
EMAIL_PASSWORD = "minha_senha"
```

Principalmente porque podemos executar:

```bash
git add .
git commit
git push
```

e acabar enviando nossa senha para:

```text
GitHub
GitLab
repositórios públicos
```

O `.env` serve justamente para separar:

```text
Código
+
Segredos
```

---

# 3. Instalar `python-dotenv`

O Django não lê arquivos `.env` sozinho.

Para isso, instalamos uma biblioteca chamada:

```text
python-dotenv
```

Com a `venv` ativada:

```powershell
python -m pip install python-dotenv
```

Podemos confirmar a instalação com:

```powershell
python -m pip show python-dotenv
```

---

# 4. Nome do pacote x nome do import

Isso pode confundir.

Para instalar:

```text
python-dotenv
```

Mas dentro do Python usamos:

```python
from dotenv import load_dotenv
```

Ou seja:

```text
Instalação:
python-dotenv

Import:
dotenv
```

---

# 5. Criar o arquivo `.env`

Na raiz do projeto, no mesmo nível do `manage.py`, criamos:

```text
.env
```

Exemplo:

```text
cinepost/
│
├── .env
├── manage.py
├── config/
└── filmes/
```

Dentro dele:

```env
CINEPOST_EMAIL_USER=seuemail@gmail.com
CINEPOST_EMAIL_PASSWORD=sua_senha_de_app
```

Não usamos a senha normal da conta Google.

Usamos uma:

```text
Senha de App
```

gerada pelo Google.

---

# 6. Senha de App do Google

Para utilizar SMTP com Gmail, usamos uma senha específica para aplicativos.

Primeiro precisamos ter:

```text
Verificação em duas etapas
```

ativada na Conta Google.

Depois criamos uma:

```text
Senha de App
```

Por exemplo:

```text
CinePost
```

O Google gera uma senha específica para o aplicativo.

Essa senha é colocada no:

```env
CINEPOST_EMAIL_PASSWORD=
```

Não devemos compartilhar essa senha nem colocá-la no Git.

---

# 7. Carregando o `.env` no Django

No começo do:

```text
config/settings.py
```

importamos:

```python
import os
from pathlib import Path

from dotenv import load_dotenv
```

O projeto já possui:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

Logo abaixo colocamos:

```python
load_dotenv(BASE_DIR / ".env")
```

Ficando:

```python
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
```

---

# 8. O que `load_dotenv()` faz?

Esta linha:

```python
load_dotenv(BASE_DIR / ".env")
```

lê:

```text
.env
```

e disponibiliza suas variáveis para o Python.

Então isso:

```env
CINEPOST_EMAIL_USER=meuemail@gmail.com
```

pode ser acessado com:

```python
os.environ["CINEPOST_EMAIL_USER"]
```

O fluxo é:

```text
.env
 ↓
python-dotenv
 ↓
load_dotenv()
 ↓
os.environ
 ↓
settings.py
```

---

# 9. Lendo as variáveis

No `settings.py`:

```python
EMAIL_USER = os.environ["CINEPOST_EMAIL_USER"]
EMAIL_PASSWORD = os.environ["CINEPOST_EMAIL_PASSWORD"]
```

Assim:

```python
os.environ["CINEPOST_EMAIL_USER"]
```

significa:

> Procure a variável chamada `CINEPOST_EMAIL_USER`.

E:

```python
os.environ["CINEPOST_EMAIL_PASSWORD"]
```

significa:

> Procure a variável chamada `CINEPOST_EMAIL_PASSWORD`.

---

# 10. Configuração de e-mail no Django 6.1

No Django 6.1 podemos configurar o envio usando:

```python
MAILERS
```

No `settings.py`:

```python
EMAIL_USER = os.environ["CINEPOST_EMAIL_USER"]
EMAIL_PASSWORD = os.environ["CINEPOST_EMAIL_PASSWORD"]


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": EMAIL_USER,
            "password": EMAIL_PASSWORD,
            "use_tls": True,
        },
    },
}

DEFAULT_FROM_EMAIL = EMAIL_USER
```

---

# 11. Entendendo o `MAILERS`

## Backend

```python
"BACKEND": "django.core.mail.backends.smtp.EmailBackend"
```

Significa:

> Vamos enviar e-mail utilizando SMTP.

---

## Host

```python
"host": "smtp.gmail.com"
```

Esse é o servidor SMTP do Gmail.

Mentalmente:

```text
Django
 ↓
smtp.gmail.com
 ↓
Gmail
```

---

## Porta

```python
"port": 587
```

É a porta usada para SMTP com TLS/STARTTLS.

---

## Usuário

```python
"username": EMAIL_USER
```

Será o e-mail carregado do `.env`.

---

## Senha

```python
"password": EMAIL_PASSWORD
```

Será a senha de app carregada do `.env`.

---

## TLS

```python
"use_tls": True
```

Ativa uma conexão protegida com TLS.

---

# 12. `DEFAULT_FROM_EMAIL`

Também definimos:

```python
DEFAULT_FROM_EMAIL = EMAIL_USER
```

Essa será a origem padrão dos e-mails enviados.

Por exemplo:

```text
De:
meuemail@gmail.com
```

---

# 13. Proteger o `.env` com `.gitignore`

O `.env` contém segredos.

Por isso ele não deve ser enviado para o Git.

No arquivo:

```text
.gitignore
```

adicionamos:

```gitignore
.env
```

Assim:

```bash
git add .
git commit
git push
```

não deve enviar o `.env`.

---

# 14. Criar `.env.example`

É uma boa prática criar também:

```text
.env.example
```

Esse arquivo pode ir para o Git.

Dentro:

```env
CINEPOST_EMAIL_USER=
CINEPOST_EMAIL_PASSWORD=
```

Ele não contém nenhuma senha.

Serve apenas para mostrar quais configurações o projeto precisa.

---

# 15. Diferença entre `.env` e `.env.example`

## `.env`

Contém dados reais:

```env
CINEPOST_EMAIL_USER=meuemail@gmail.com
CINEPOST_EMAIL_PASSWORD=minha_senha_de_app
```

Não vai para o Git.

---

## `.env.example`

Contém apenas a estrutura:

```env
CINEPOST_EMAIL_USER=
CINEPOST_EMAIL_PASSWORD=
```

Pode ir para o Git.

É útil para outras pessoas saberem quais variáveis precisam criar.

---

# 16. Estrutura recomendada

```text
cinepost/
│
├── .env
│   └── dados reais
│
├── .env.example
│   └── modelo das variáveis
│
├── .gitignore
│   └── impede envio do .env
│
├── manage.py
│
└── config/
    └── settings.py
        └── lê o .env
```

---

# 17. Testar se o Django está configurado corretamente

Antes de testar e-mail, podemos executar:

```powershell
python manage.py check
```

Se estiver tudo certo:

```text
System check identified no issues
```

Isso significa que o Django conseguiu carregar as configurações sem encontrar problemas estruturais.

---

# 18. Erro de variável inexistente

Se aparecer algo parecido com:

```text
KeyError: 'CINEPOST_EMAIL_USER'
```

significa que:

```python
os.environ["CINEPOST_EMAIL_USER"]
```

não encontrou essa variável.

Devemos conferir:

1. Se o `.env` existe.
2. Se está na raiz do projeto.
3. Se escrevemos corretamente:

```env
CINEPOST_EMAIL_USER=
```

4. Se temos:

```python
load_dotenv(BASE_DIR / ".env")
```

antes de tentar acessar a variável.

---

# 19. Testar o envio de e-mail

No Django 6.1 podemos usar:

```powershell
python manage.py sendtestemail destinatario@gmail.com
```

Exemplo:

```powershell
python manage.py sendtestemail meuemail@gmail.com
```

O Django tenta enviar um e-mail utilizando a configuração:

```python
MAILERS["default"]
```

---

# 20. Fluxo do teste

Quando executamos:

```powershell
python manage.py sendtestemail meuemail@gmail.com
```

acontece aproximadamente:

```text
manage.py
 ↓
Django
 ↓
MAILERS["default"]
 ↓
SMTP Backend
 ↓
smtp.gmail.com
 ↓
porta 587
 ↓
TLS
 ↓
login com Gmail
 ↓
senha de app
 ↓
e-mail enviado
```

---

# 21. Testando o servidor SMTP pela rede

Se aparecer um erro relacionado a:

```text
getaddrinfo failed
```

podemos verificar se o computador encontra o servidor do Gmail.

No PowerShell:

```powershell
nslookup smtp.gmail.com
```

Se aparecer endereço IP, significa que o DNS conseguiu encontrar:

```text
smtp.gmail.com
```

---

# 22. Testando a porta 587

Também podemos testar:

```powershell
Test-NetConnection smtp.gmail.com -Port 587
```

O ideal é aparecer:

```text
TcpTestSucceeded : True
```

Isso significa:

```text
Computador
 ↓
conseguiu alcançar
 ↓
smtp.gmail.com
 ↓
porta 587
```

Se aparecer:

```text
False
```

o problema pode estar relacionado a:

```text
internet
DNS
firewall
antivírus
rede
bloqueio de porta
```

e não necessariamente ao Django.

---

# 23. Testando manualmente com `send_mail()`

Também podemos entrar no shell do Django:

```powershell
python manage.py shell
```

Depois:

```python
from django.core.mail import send_mail
```

E testar:

```python
send_mail(
    "Teste do CinePost",
    "Se você recebeu esta mensagem, o Django está enviando e-mails corretamente.",
    None,
    ["destinatario@gmail.com"],
)
```

---

# 24. Entendendo `send_mail()`

A estrutura básica é:

```python
send_mail(
    assunto,
    mensagem,
    remetente,
    destinatarios,
)
```

Exemplo:

```python
send_mail(
    "CinePost",
    "Veja este filme!",
    None,
    ["amigo@gmail.com"],
)
```

---

# 25. Por que usamos `None` como remetente?

Neste exemplo:

```python
send_mail(
    "Teste",
    "Mensagem",
    None,
    ["destinatario@gmail.com"],
)
```

o terceiro argumento representa:

```text
from_email
```

Como colocamos:

```python
None
```

o Django utiliza:

```python
DEFAULT_FROM_EMAIL
```

que configuramos como:

```python
DEFAULT_FROM_EMAIL = EMAIL_USER
```

---

# 26. Resultado do `send_mail()`

Se o envio funcionar, normalmente o retorno será:

```python
1
```

Isso significa:

> uma mensagem foi enviada.

---

# 27. SMTP

SMTP significa:

```text
Simple Mail Transfer Protocol
```

É o protocolo usado para envio de e-mails.

O Django não entrega o e-mail diretamente ao destinatário.

O fluxo é:

```text
Django
 ↓
SMTP
 ↓
Gmail
 ↓
Internet
 ↓
destinatário
```

---

# 28. Por que usar Gmail?

Neste projeto usamos:

```text
smtp.gmail.com
```

porque o Gmail oferece um servidor SMTP que podemos utilizar para aprender e testar.

Em sistemas reais também poderíamos utilizar serviços especializados de envio de e-mails.

---

# 29. Segurança

Nunca devemos colocar diretamente no código:

```python
password = "minha_senha"
```

Nem compartilhar:

```text
Senha normal do Gmail
Senha de App
SECRET_KEY
API Keys
Tokens
```

Essas informações devem ficar fora do código.

Exemplo:

```env
CINEPOST_EMAIL_PASSWORD=...
```

---

# 30. Outras informações que podem ficar no `.env`

O mesmo padrão pode ser utilizado futuramente para:

```env
SECRET_KEY=
DATABASE_PASSWORD=
API_KEY=
EMAIL_PASSWORD=
TOKEN=
```

Então o `.env` não serve somente para e-mail.

É uma forma genérica de separar configurações sensíveis do código.

---

# 31. Fluxo completo da configuração

```text
1. Ativar verificação em duas etapas no Google
             ↓
2. Criar uma Senha de App
             ↓
3. Instalar python-dotenv
             ↓
4. Criar .env
             ↓
5. Salvar e-mail e senha de app
             ↓
6. load_dotenv()
             ↓
7. os.environ
             ↓
8. MAILERS no settings.py
             ↓
9. Gmail SMTP
             ↓
10. Testar com manage.py check
             ↓
11. Testar com sendtestemail
             ↓
12. E-mail recebido
```

---

# 32. Código final do `settings.py`

Parte relevante:

```python
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


EMAIL_USER = os.environ["CINEPOST_EMAIL_USER"]
EMAIL_PASSWORD = os.environ["CINEPOST_EMAIL_PASSWORD"]


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": EMAIL_USER,
            "password": EMAIL_PASSWORD,
            "use_tls": True,
        },
    },
}

DEFAULT_FROM_EMAIL = EMAIL_USER
```

---

# 33. `.env`

```env
CINEPOST_EMAIL_USER=seuemail@gmail.com
CINEPOST_EMAIL_PASSWORD=sua_senha_de_app
```

---

# 34. `.env.example`

```env
CINEPOST_EMAIL_USER=
CINEPOST_EMAIL_PASSWORD=
```

---

# 35. `.gitignore`

```gitignore
.env
```

---

# 36. Comandos importantes

Instalar:

```powershell
python -m pip install python-dotenv
```

Verificar instalação:

```powershell
python -m pip show python-dotenv
```

Verificar Django:

```powershell
python manage.py check
```

Testar envio:

```powershell
python manage.py sendtestemail destinatario@gmail.com
```

Verificar DNS:

```powershell
nslookup smtp.gmail.com
```

Verificar porta SMTP:

```powershell
Test-NetConnection smtp.gmail.com -Port 587
```

Abrir shell do Django:

```powershell
python manage.py shell
```

---

# 37. Mapa mental final

```text
.env
│
├── EMAIL_USER
└── EMAIL_PASSWORD
        ↓
python-dotenv
        ↓
load_dotenv()
        ↓
os.environ
        ↓
settings.py
        ↓
MAILERS
        ↓
SMTP Backend
        ↓
smtp.gmail.com
        ↓
Gmail
        ↓
Destinatário
```

---

# Resumo para decorar

## `.env`

Guarda informações sensíveis fora do código.

## `python-dotenv`

Lê o arquivo `.env`.

## `load_dotenv()`

Carrega as variáveis do `.env`.

## `os.environ`

Permite acessar essas variáveis no Python.

## `MAILERS`

Configura como o Django enviará os e-mails.

## SMTP

É o protocolo utilizado para enviar e-mails.

## Senha de App

É a credencial específica que usamos para permitir que o Django se autentique no Gmail.

## `.gitignore`

Impede que nosso `.env` seja enviado para o repositório.

## `.env.example`

Mostra quais variáveis o projeto precisa sem revelar informações privadas.

---

# Ideia principal

> O `.env` mantém credenciais fora do código.

> O `python-dotenv` carrega essas credenciais para o ambiente Python.

> O Django lê essas informações no `settings.py`.

> O `MAILERS` configura o servidor SMTP.

> O Gmail recebe a mensagem do Django e faz o envio para o destinatário.

O fluxo completo é:

```text
.env
 ↓
python-dotenv
 ↓
settings.py
 ↓
MAILERS
 ↓
SMTP
 ↓
Gmail
 ↓
E-mail enviado
```