# Django — Criando um Projeto do Zero no Windows

## Objetivo

Este material serve como referência para começar um novo projeto Django do zero usando:

```text
Windows
VS Code
PowerShell
Python
Django
```

O fluxo geral será:

```text
Criar pasta
↓
Criar ambiente virtual
↓
Ativar ambiente
↓
Instalar Django
↓
Criar projeto
↓
Criar app
↓
Configurar
↓
Migrations
↓
Criar superusuário
↓
Executar servidor
```

---

# 1. Criar a pasta do projeto

No terminal:

```powershell
mkdir meu_projeto
```

Entre nela:

```powershell
cd meu_projeto
```

Exemplo:

```powershell
mkdir cinepost
cd cinepost
```

---

# 2. Criar o ambiente virtual

Execute:

```powershell
python -m venv venv
```

Isso cria:

```text
meu_projeto/
└── venv/
```

---

# O que é o ambiente virtual?

O ambiente virtual isola as bibliotecas daquele projeto.

Imagine:

```text
Projeto A
└── Django 6

Projeto B
└── Django 5

Projeto C
└── Flask
```

Cada projeto pode possuir suas próprias dependências.

Sem ambiente virtual, tudo ficaria instalado globalmente no computador.

---

# 3. Ativar o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Quando funcionar, normalmente o terminal ficará parecido com:

```text
(venv) PS C:\...\meu_projeto>
```

Isso significa:

```text
ambiente virtual ativo ✅
```

---

# 4. Desativar o ambiente virtual

Quando quiser sair:

```powershell
deactivate
```

---

# 5. Instalar Django

Com o ambiente virtual ativado:

```powershell
python -m pip install Django
```

---

# Verificar a versão

```powershell
python -m django --version
```

Exemplo:

```text
6.1
```

O livro utilizado durante os estudos foi escrito para Django 5, mas o projeto CinePost foi desenvolvido utilizando Django 6.1.

---

# 6. Atualizar o `pip`

Opcionalmente:

```powershell
python -m pip install --upgrade pip
```

---

# 7. Criar o projeto Django

Uma organização que gosto de utilizar é:

```powershell
django-admin startproject config .
```

O ponto:

```text
.
```

significa:

```text
crie o projeto nesta pasta
```

Isso evita criar uma pasta extra desnecessária.

---

# Estrutura inicial

Depois:

```text
meu_projeto/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── venv/
```

---

# 8. O que é `config`?

A pasta:

```text
config/
```

representa a configuração geral do projeto.

Ela possui principalmente:

```text
settings.py
urls.py
asgi.py
wsgi.py
```

---

# Projeto x App

Uma distinção muito importante.

## Projeto

Representa o site/sistema completo.

Exemplo:

```text
CinePost
```

---

## App

Representa uma funcionalidade ou módulo.

Exemplo:

```text
filmes
contas
pagamentos
notificacoes
```

Mentalmente:

```text
CinePost
├── filmes
├── contas
└── outros apps
```

---

# 9. Criar um app

Exemplo:

```powershell
python manage.py startapp contas
```

Estrutura:

```text
contas/
├── migrations/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

---

# 10. Registrar o app

Abra:

```text
config/settings.py
```

Procure:

```python
INSTALLED_APPS
```

Adicione:

```python
"contas.apps.ContasConfig",
```

Exemplo:

```python
INSTALLED_APPS = [
    "contas.apps.ContasConfig",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

---

# Por que registrar o app?

Criar:

```powershell
python manage.py startapp contas
```

apenas cria os arquivos.

O Django também precisa saber:

```text
esse app faz parte deste projeto
```

Isso é feito através de:

```python
INSTALLED_APPS
```

---

# 11. Apps que já vêm com Django

Um projeto novo normalmente inclui:

```python
"django.contrib.admin"
"django.contrib.auth"
"django.contrib.contenttypes"
"django.contrib.sessions"
"django.contrib.messages"
"django.contrib.staticfiles"
```

---

# `django.contrib.admin`

Fornece:

```text
Django Admin
```

---

# `django.contrib.auth`

Fornece:

```text
usuários
senhas
login
logout
permissões
grupos
```

---

# `django.contrib.sessions`

Mantém sessões dos usuários.

Exemplo:

```text
usuário faz login
↓
navega para outra página
↓
continua logado
```

---

# 12. Executar migrations iniciais

Depois de criar o projeto:

```powershell
python manage.py migrate
```

Isso cria as tabelas necessárias para os aplicativos padrão do Django.

Exemplo:

```text
auth
admin
sessions
contenttypes
```

---

# O que são migrations?

Migrations representam o histórico da estrutura do banco.

Mentalmente:

```text
Models
↓
makemigrations
↓
arquivos de migration
↓
migrate
↓
banco de dados
```

---

# `makemigrations`

Quando alteramos nossos Models:

```powershell
python manage.py makemigrations
```

Significa:

```text
analise os Models
↓
descubra mudanças
↓
crie instruções
```

Analogia:

```text
makemigrations
= criar a planta
```

---

# `migrate`

Depois:

```powershell
python manage.py migrate
```

Significa:

```text
pegue as migrations
↓
execute no banco
```

Analogia:

```text
migrate
= executar a planta
```

---

# 13. Criar um superusuário

Para acessar o Django Admin:

```powershell
python manage.py createsuperuser
```

O Django pedirá:

```text
Username:
Email:
Password:
Password again:
```

A senha não aparece enquanto você digita.

Isso é normal.

---

# 14. Executar o servidor

```powershell
python manage.py runserver
```

Normalmente:

```text
http://127.0.0.1:8000/
```

---

# Abrir o Admin

```text
http://127.0.0.1:8000/admin/
```

Entre utilizando o superusuário criado.

---

# 15. Parar o servidor

No terminal:

```text
Ctrl + C
```

---

# 16. Criar `requirements.txt`

Depois de instalar as bibliotecas do projeto:

```powershell
pip freeze > requirements.txt
```

Exemplo:

```text
Django==...
psycopg==...
django-taggit==...
```

---

# Para instalar as dependências posteriormente

Em outro computador ou ambiente:

```powershell
pip install -r requirements.txt
```

---

# 17. Estrutura sugerida

Um projeto pode começar assim:

```text
meu_projeto/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── contas/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── venv/
├── manage.py
└── requirements.txt
```

---

# 18. Criando `urls.py` dentro do app

Apps novos não vêm necessariamente com `urls.py`.

Podemos criar:

```text
contas/urls.py
```

Exemplo:

```python
from django.urls import path

from . import views


app_name = "contas"


urlpatterns = [
]
```

---

# 19. Ligando URLs do app ao projeto

No:

```text
config/urls.py
```

importe:

```python
from django.urls import include, path
```

Depois:

```python
urlpatterns = [
    path(
        "contas/",
        include("contas.urls"),
    ),
]
```

Mentalmente:

```text
/contas/
↓
config/urls.py
↓
contas/urls.py
↓
view
```

---

# 20. Ordem básica de criação

Uma sequência prática para projetos futuros:

```text
1. mkdir projeto

2. cd projeto

3. python -m venv venv

4. .\venv\Scripts\Activate.ps1

5. pip install Django

6. django-admin startproject config .

7. python manage.py startapp nome_app

8. adicionar app em INSTALLED_APPS

9. python manage.py migrate

10. python manage.py createsuperuser

11. python manage.py runserver
```

---

# Comandos reunidos

```powershell
mkdir meu_projeto
cd meu_projeto

python -m venv venv

.\venv\Scripts\Activate.ps1

python -m pip install Django

django-admin startproject config .

python manage.py startapp contas

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

---

# Resumo mental

```text
venv
= ambiente isolado
```

```text
pip
= instala bibliotecas Python
```

```text
startproject
= cria o projeto Django
```

```text
startapp
= cria um módulo do projeto
```

```text
INSTALLED_APPS
= informa quais apps fazem parte do projeto
```

```text
makemigrations
= cria instruções de alteração do banco
```

```text
migrate
= executa essas instruções
```

```text
createsuperuser
= cria usuário administrativo
```

```text
runserver
= inicia servidor de desenvolvimento
```

---

# Fluxo completo

```text
Python
↓
venv
↓
Django
↓
Projeto
↓
Apps
↓
Models
↓
Migrations
↓
Banco
↓
Views
↓
Templates
↓
URLs
↓
Navegador
```