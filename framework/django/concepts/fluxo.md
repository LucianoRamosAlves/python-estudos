# Fluxo básico do Django

## 1. Criar o projeto

```bash
django-admin startproject config .
```

Cria a estrutura principal do Django.

```text
config/
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py
```

---

## 2. Criar um App

```bash
python manage.py startapp filmes
```

O App é um módulo do projeto.

```text
Projeto = sistema completo
App = parte do sistema
```

Exemplo:

```text
CinePost
└── filmes
```

---

## 3. Criar uma View

A View recebe a requisição e executa a lógica.

```python
from django.http import HttpResponse


def inicio(request):
    return HttpResponse("Olá, CinePost!")
```

A View pode:

- consultar o banco;
- fazer filtros;
- validar dados;
- executar lógica;
- retornar uma resposta.

---

## 4. Criar a URL do App

`filmes/urls.py`:

```python
from django.urls import path

from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
]
```

O `path()` pode ser lido assim:

```text
path(
    caminho,
    view,
    nome_da_rota
)
```

Exemplo:

```python
path("", views.inicio, name="inicio")
```

- `""` → caminho;
- `views.inicio` → lógica executada;
- `name="inicio"` → apelido interno da rota.

---

## 5. Conectar o App ao projeto

`config/urls.py`:

```python
from django.urls import include, path


urlpatterns = [
    path("filmes/", include("filmes.urls")),
]
```

Isso significa:

> Tudo que começar com `/filmes/` deve procurar o restante da rota em `filmes/urls.py`.

Então:

```text
"filmes/" + ""
=
/filmes/
```

---

## 6. Fluxo de uma requisição

Quando o usuário acessa:

```text
/filmes/
```

acontece:

```text
Navegador
↓
config/urls.py
↓
filmes/urls.py
↓
View
↓
Response
↓
Navegador
```

Ou:

```text
URL → View → Resposta
```

---

## 7. Quando existe Template

Em vez de retornar texto:

```python
return HttpResponse("Olá")
```

podemos usar:

```python
return render(
    request,
    "filmes/inicio.html",
)
```

Fluxo:

```text
URL
↓
View
↓
Template
↓
HTML
↓
Response
```

---

## 8. Quando existe banco de dados

A View pode usar a ORM:

```python
def post_list(request):
    posts = PostFilme.publicados.all()

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Fluxo completo:

```text
Usuário
↓
URL
↓
View
↓
ORM
↓
Banco
↓
View
↓
Template
↓
HttpResponse
↓
Usuário
```

---

# Papel de cada parte

```text
settings.py
→ configura o projeto

urls.py
→ encontra a View

views.py
→ executa a lógica

models.py / ORM
→ trabalha com o banco

templates/
→ monta o HTML

static/
→ CSS, JS e imagens
```

---

# Regra principal

> **A URL decide qual View executar.**

> **A View decide o que fazer.**

> **A ORM busca dados quando necessário.**

> **O Template decide como mostrar o resultado.**

Resumo final:

```text
REQUEST
↓
URL
↓
VIEW
↓
ORM / BANCO
↓
TEMPLATE
↓
RESPONSE
```