# Django — Template Tags Personalizadas

## Objetivo

O Django já possui várias template tags prontas:

```django
{% if %}
{% for %}
{% include %}
{% block %}
```

Mas também podemos criar nossas próprias tags para executar funcionalidades reutilizáveis nos templates.

No CinePost começamos usando dois tipos:

```text
simple_tag
inclusion_tag
```

---

# Estrutura necessária

Dentro do app `filmes` criamos:

```text
filmes/
└── templatetags/
    ├── __init__.py
    └── filmes_tags.py
```

O arquivo:

```text
filmes_tags.py
```

é carregado no template com:

```django
{% load filmes_tags %}
```

---

# Registrando a biblioteca

Dentro de `filmes_tags.py`:

```python
from django import template

from ..models import PostFilme


register = template.Library()
```

Esta linha:

```python
register = template.Library()
```

cria a biblioteca onde nossas tags personalizadas serão registradas.

---

# `simple_tag`

A primeira tag criada foi:

```python
@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()
```

Ela pode ser usada no template:

```django
{% total_posts %}
```

Exemplo de resultado:

```text
12
```

---

## Como funciona

```text
{% total_posts %}
↓
Django executa total_posts()
↓
PostFilme.publicados.count()
↓
retorna um valor
↓
12
```

A `simple_tag` é indicada quando queremos retornar um valor simples.

---

# `inclusion_tag`

Depois criamos uma tag para mostrar os últimos posts:

```python
@register.inclusion_tag("filmes/post/ultimos_posts.html")
def mostrar_ultimos_posts(quantidade=5):

    ultimos_posts = PostFilme.publicados.order_by(
        "-publicado_em"
    )[:quantidade]

    return {
        "ultimos_posts": ultimos_posts
    }
```

---

# O que `inclusion_tag` faz?

Diferente da `simple_tag`, ela não retorna apenas um valor.

Ela:

```text
executa Python
↓
busca dados
↓
cria um contexto
↓
envia para outro template
↓
renderiza esse template
```

---

# Template utilizado pela `inclusion_tag`

Criamos:

```text
filmes/templates/filmes/post/ultimos_posts.html
```

Com:

```django
<ul>

    {% for post in ultimos_posts %}

        <li>
            <a href="{{ post.get_absolute_url }}">
                {{ post.titulo }}
            </a>
        </li>

    {% endfor %}

</ul>
```

A variável:

```django
ultimos_posts
```

vem deste dicionário:

```python
return {
    "ultimos_posts": ultimos_posts
}
```

---

# Usando a `inclusion_tag`

No template podemos chamar:

```django
{% mostrar_ultimos_posts %}
```

Nesse caso será usada a quantidade padrão:

```python
quantidade=5
```

Então serão mostrados 5 posts.

Também podemos passar outro valor:

```django
{% mostrar_ultimos_posts 3 %}
```

Nesse caso:

```text
quantidade = 3
```

e serão mostrados apenas os 3 posts mais recentes.

---

# QuerySet utilizado

```python
PostFilme.publicados.order_by(
    "-publicado_em"
)[:quantidade]
```

Isso significa:

```text
PostFilme publicados
↓
ordena pelos mais recentes
↓
limita pela quantidade escolhida
```

O `-` em:

```python
"-publicado_em"
```

significa ordem decrescente.

Ou seja:

```text
mais recente
↓
mais antigo
```

---

# Diferença entre `simple_tag` e `inclusion_tag`

## `simple_tag`

Exemplo:

```python
@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()
```

Uso:

```django
{% total_posts %}
```

Retorna algo simples:

```text
12
```

Fluxo:

```text
Python
↓
valor
↓
template
```

---

## `inclusion_tag`

Exemplo:

```python
@register.inclusion_tag("filmes/post/ultimos_posts.html")
def mostrar_ultimos_posts(quantidade=5):

    ultimos_posts = PostFilme.publicados.order_by(
        "-publicado_em"
    )[:quantidade]

    return {
        "ultimos_posts": ultimos_posts
    }
```

Uso:

```django
{% mostrar_ultimos_posts 3 %}
```

Ela pode gerar um bloco inteiro:

```text
Últimos posts

- Interestelar
- Corra
- Duna
```

Fluxo:

```text
Python
↓
dicionário de contexto
↓
outro template
↓
HTML renderizado
```

---

# Comparação rápida

```text
simple_tag
→ retorna um valor

inclusion_tag
→ renderiza um template
```

Exemplo:

```django
{% total_posts %}
```

pode resultar em:

```text
12
```

Enquanto:

```django
{% mostrar_ultimos_posts 3 %}
```

pode resultar em:

```text
Interestelar
Corra
Duna
```

---

# Por que usar `inclusion_tag`?

Imagine que queremos mostrar os últimos posts em várias páginas:

```text
Página inicial
Detalhes do filme
Página de tags
Outra página
```

Sem `inclusion_tag`, poderíamos ter que repetir a consulta nas Views.

Com ela:

```django
{% mostrar_ultimos_posts 3 %}
```

pode ser reutilizada sempre que necessário.

---

# Arquivo atual `filmes_tags.py`

Até aqui temos:

```python
from django import template

from ..models import PostFilme


register = template.Library()


@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()


@register.inclusion_tag("filmes/post/ultimos_posts.html")
def mostrar_ultimos_posts(quantidade=5):

    ultimos_posts = PostFilme.publicados.order_by(
        "-publicado_em"
    )[:quantidade]

    return {
        "ultimos_posts": ultimos_posts
    }
```

---

# Carregando no template

Antes de usar as tags:

```django
{% load filmes_tags %}
```

Depois podemos usar:

```django
{% total_posts %}
```

e:

```django
{% mostrar_ultimos_posts 3 %}
```

---

# Erro encontrado

Ao criar a biblioteca tivemos o erro:

```text
'filmes_tags' is not a registered tag library
```

No nosso caso, o código estava correto.

O problema era que o servidor ainda não havia sido reiniciado.

Depois de criar novos arquivos dentro de:

```text
templatetags/
```

é recomendável parar o servidor:

```text
Ctrl + C
```

e iniciar novamente:

```powershell
python manage.py runserver
```

Depois disso o Django reconheceu:

```django
{% load filmes_tags %}
```

---

# Resumo mental

```text
templatetags/
↓
filmes_tags.py
↓
register = template.Library()
↓
criamos nossas tags
```

Para valor simples:

```text
@register.simple_tag
↓
função Python
↓
retorna valor
```

Para um bloco reutilizável de HTML:

```text
@register.inclusion_tag
↓
função Python
↓
retorna contexto
↓
outro template
↓
HTML pronto
```

---

# Principal diferença

```text
simple_tag
= quero um resultado

inclusion_tag
= quero renderizar um componente
```

No CinePost:

```django
{% total_posts %}
```

é uma `simple_tag`.

```django
{% mostrar_ultimos_posts 3 %}
```

é uma `inclusion_tag`.