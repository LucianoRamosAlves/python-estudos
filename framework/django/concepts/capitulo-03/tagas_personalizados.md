# Django — Template Tags Personalizadas

## O que são template tags personalizadas?

O Django já possui várias template tags prontas, como:

```django
{% if %}
{% for %}
{% block %}
{% include %}
```

Também possui filtros prontos, como:

```django
{{ texto|linebreaks }}
{{ texto|truncatewords:30 }}
{{ total|pluralize }}
```

Mas o Django também permite criar nossas próprias tags e filtros.

Isso é útil quando queremos colocar uma lógica reutilizável diretamente nos templates.

Exemplo:

```django
{% total_posts %}
```

Essa tag personalizada pode buscar no banco quantos posts publicados existem.

---

# Tipos principais

O Django fornece duas formas muito comuns de criar template tags.

## `simple_tag`

Executa uma lógica Python e retorna um valor.

Exemplo:

```django
{% total_posts %}
```

Pode retornar:

```text
12
```

Mentalmente:

```text
simple_tag
↓
executa Python
↓
retorna um valor
```

---

## `inclusion_tag`

Executa uma lógica e renderiza outro template.

Exemplo conceitual:

```django
{% ultimos_posts %}
```

Pode gerar:

```text
Últimos posts
- Interestelar
- Corra
- Duna
```

Mentalmente:

```text
inclusion_tag
↓
executa Python
↓
busca dados
↓
envia para outro template
↓
renderiza esse template
```

Ainda não usamos `inclusion_tag`, apenas conhecemos o conceito.

---

# Criando a estrutura

As template tags precisam ficar dentro de um app Django.

No CinePost criamos:

```text
filmes/
├── models.py
├── views.py
├── urls.py
├── ...
└── templatetags/
    ├── __init__.py
    └── filmes_tags.py
```

A pasta precisa se chamar exatamente:

```text
templatetags
```

---

## `__init__.py`

Criamos:

```text
filmes/templatetags/__init__.py
```

Ele pode ficar vazio.

Ele ajuda a identificar aquela pasta como um módulo Python.

---

# Nome do arquivo

Criamos:

```text
filmes_tags.py
```

Esse nome é importante porque será usado no template:

```django
{% load filmes_tags %}
```

Então:

```text
filmes_tags.py
↓
{% load filmes_tags %}
```

---

# Criando a primeira tag personalizada

Dentro de:

```text
filmes/templatetags/filmes_tags.py
```

colocamos:

```python
from django import template

from ..models import PostFilme


register = template.Library()


@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()
```

---

# Entendendo cada parte

## Importando `template`

```python
from django import template
```

Importa as ferramentas usadas para criar template tags personalizadas.

---

## Importando o Model

```python
from ..models import PostFilme
```

Importamos nosso `PostFilme` para poder fazer consultas ao banco.

---

# `template.Library()`

Criamos:

```python
register = template.Library()
```

Essa linha é muito importante.

Cada módulo de template tags precisa ter uma biblioteca onde suas tags e filtros serão registrados.

Mentalmente:

```text
filmes_tags.py
↓
register
↓
biblioteca de tags personalizadas
```

---

# `@register.simple_tag`

Criamos:

```python
@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()
```

O decorator:

```python
@register.simple_tag
```

transforma a função Python:

```python
total_posts()
```

em uma template tag:

```django
{% total_posts %}
```

---

# Nome da tag

Por padrão, o Django utiliza o nome da função.

Então:

```python
def total_posts():
```

vira:

```django
{% total_posts %}
```

Também seria possível registrar com outro nome:

```python
@register.simple_tag(name="quantidade_posts")
def total_posts():
    ...
```

E usar:

```django
{% quantidade_posts %}
```

Mas não precisamos disso agora.

---

# O que nossa tag faz?

Nossa função:

```python
def total_posts():
    return PostFilme.publicados.count()
```

usa nosso manager:

```python
PostFilme.publicados
```

e conta somente os posts publicados.

Exemplo:

```text
15 posts no banco

12 publicados
3 rascunhos
```

Nossa tag retorna:

```text
12
```

---

# Carregando a biblioteca no template

Antes de usar nossas tags, precisamos carregar o módulo.

No `base.html`:

```django
{% load filmes_tags %}
```

Também podemos ter:

```django
{% load filmes_tags %}
{% load static %}
```

Depois disso podemos usar:

```django
{% total_posts %}
```

---

# Usando no `base.html`

Exemplo:

```django
<p>
    Já publicamos {% total_posts %} posts.
</p>
```

Se existirem 8 posts publicados:

```text
Já publicamos 8 posts.
```

---

# Por que usar no `base.html`?

Como `base.html` é herdado por várias páginas:

```django
{% extends "filmes/base.html" %}
```

podemos mostrar essa informação em várias partes do site sem precisar modificar todas as Views.

Exemplo:

```text
post_list
post_detail
comentários
recomendação
...
```

Todas podem herdar o mesmo `base.html`.

---

# Principal vantagem

Sem uma template tag personalizada, poderíamos ter que fazer isso em várias Views:

```python
total_posts = PostFilme.publicados.count()
```

e depois:

```python
{
    "total_posts": total_posts
}
```

em vários `render()`.

Com nossa tag:

```django
{% total_posts %}
```

a própria tag faz a consulta.

Então:

```text
lógica reutilizável
↓
filmes_tags.py
↓
template carrega
↓
{% total_posts %}
```

---

# Erro que encontramos

Recebemos:

```text
'filmes_tags' is not a registered tag library
```

O Django ainda não estava reconhecendo:

```text
filmes/templatetags/filmes_tags.py
```

No nosso caso, o problema era simples:

> O servidor ainda não tinha sido reiniciado depois da criação do novo módulo.

---

# Reiniciando o servidor

Depois de criar uma nova biblioteca de template tags, é importante parar o servidor:

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

normalmente.

---

# Se esse erro aparecer novamente

Confira:

```text
filmes/
└── templatetags/
    ├── __init__.py
    └── filmes_tags.py
```

Depois confira se no template está:

```django
{% load filmes_tags %}
```

E reinicie:

```powershell
python manage.py runserver
```

---

# Fluxo completo

```text
Criamos templatetags/
↓
criamos __init__.py
↓
criamos filmes_tags.py
↓
criamos register = template.Library()
↓
criamos função Python
↓
@register.simple_tag
↓
função vira template tag
↓
{% load filmes_tags %}
↓
{% total_posts %}
↓
Django executa PostFilme.publicados.count()
↓
template mostra o resultado
```

---

# Resumo dos conceitos

## Pasta obrigatória

```text
templatetags/
```

---

## Biblioteca de tags

```python
register = template.Library()
```

---

## Criar uma `simple_tag`

```python
@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()
```

---

## Carregar no template

```django
{% load filmes_tags %}
```

---

## Usar a tag

```django
{% total_posts %}
```

---

# Resumo mental

```text
Python normal
↓
@register.simple_tag
↓
vira funcionalidade do template
↓
{% total_posts %}
```

A ideia principal é:

> Custom template tags permitem criar funcionalidades próprias e reutilizáveis para os templates sem precisar repetir a mesma lógica em várias Views.