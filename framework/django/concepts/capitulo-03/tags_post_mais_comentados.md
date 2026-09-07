# Django — Template Tag para Posts Mais Comentados

## Objetivo

Criamos uma template tag personalizada para mostrar os posts com mais comentários.

A ideia é:

```text
buscar posts publicados
↓
contar comentários
↓
ordenar pelos mais comentados
↓
limitar a quantidade
↓
mostrar no template
```

---

# Importando `Count`

No arquivo:

```text
filmes/templatetags/filmes_tags.py
```

adicionamos:

```python
from django.db.models import Count, Q
```

`Count` serve para fazer contagens no ORM.

`Q` foi usado para contar somente comentários ativos.

---

# Criando a tag

Adicionamos:

```python
@register.simple_tag
def posts_mais_comentados(quantidade=5):
    return (
        PostFilme.publicados
        .annotate(
            total_comentarios=Count(
                "comentarios",
                filter=Q(comentarios__ativo=True),
            )
        )
        .order_by("-total_comentarios")[:quantidade]
    )
```

---

# O que essa consulta faz?

Primeiro:

```python
PostFilme.publicados
```

pega somente posts publicados.

Depois:

```python
.annotate(
    total_comentarios=Count(...)
)
```

cria um campo calculado temporário:

```text
total_comentarios
```

Exemplo:

```text
Interestelar
total_comentarios = 8

Corra
total_comentarios = 5
```

Esse campo não existe no Model.

Ele só existe durante esse QuerySet.

---

# Contando somente comentários ativos

Usamos:

```python
filter=Q(comentarios__ativo=True)
```

Assim comentários desativados pelo administrador não entram na contagem.

Exemplo:

```text
8 comentários no banco
2 inativos

total_comentarios = 6
```

---

# Ordenando

Usamos:

```python
.order_by("-total_comentarios")
```

O `-` significa ordem decrescente.

Então:

```text
8 comentários
5 comentários
3 comentários
1 comentário
```

---

# Limitando resultados

Usamos:

```python
[:quantidade]
```

Como o padrão é:

```python
quantidade=5
```

a tag retorna no máximo 5 posts.

Também podemos pedir apenas 3:

```django
{% posts_mais_comentados 3 as mais_comentados %}
```

---

# Nova forma de usar `simple_tag`

Antes usamos:

```django
{% total_posts %}
```

e o resultado era exibido diretamente.

Agora usamos:

```django
{% posts_mais_comentados as mais_comentados %}
```

O `as` guarda o resultado em uma variável.

Então:

```text
posts_mais_comentados
↓
retorna QuerySet
↓
as mais_comentados
↓
variável disponível no template
```

---

# Usando a variável

Depois podemos fazer:

```django
{% for post in mais_comentados %}

    {{ post.titulo }}

{% endfor %}
```

Também podemos acessar o campo criado pelo `annotate()`:

```django
{{ post.total_comentarios }}
```

---

# Exemplo no template

```django
{% posts_mais_comentados 5 as mais_comentados %}

{% for post in mais_comentados %}

    <a href="{{ post.get_absolute_url }}">
        {{ post.titulo }}
    </a>

    {{ post.total_comentarios }}
    comentário{{ post.total_comentarios|pluralize }}

{% empty %}

    Ainda não existem publicações.

{% endfor %}
```

---

# Bootstrap

No CinePost usamos cards para mostrar o ranking.

Exemplo visual:

```text
Posts mais comentados

┌─────────────────────────────┐
│ Interestelar          [1]   │
│ 8 comentários               │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Corra                 [2]   │
│ 5 comentários               │
└─────────────────────────────┘
```

O ranking vem de:

```django
{{ forloop.counter }}
```

E a quantidade de comentários vem de:

```django
{{ post.total_comentarios }}
```

---

# Diferença para as tags anteriores

## `simple_tag` direto

```django
{% total_posts %}
```

Retorna e mostra diretamente:

```text
12
```

---

## `inclusion_tag`

```django
{% mostrar_ultimos_posts 3 %}
```

Executa uma consulta e renderiza outro template.

Fluxo:

```text
Python
↓
contexto
↓
template separado
↓
HTML
```

---

## `simple_tag` usando `as`

```django
{% posts_mais_comentados as mais_comentados %}
```

Retorna um valor ou QuerySet e guarda em uma variável.

Fluxo:

```text
Python
↓
QuerySet
↓
variável
↓
template decide como exibir
```

---

# Resumo mental

```text
@register.simple_tag
↓
posts_mais_comentados()
↓
PostFilme.publicados
↓
annotate()
↓
Count("comentarios")
↓
total_comentarios
↓
order_by("-total_comentarios")
↓
[:quantidade]
↓
QuerySet
↓
as mais_comentados
↓
for no template
```

---

# Principal aprendizado

Uma `simple_tag` não precisa obrigatoriamente imprimir o resultado imediatamente.

Ela também pode retornar um QuerySet:

```python
return QuerySet
```

e o template pode armazená-lo com:

```django
{% minha_tag as variavel %}
```

Depois essa variável pode ser utilizada normalmente:

```django
{% for objeto in variavel %}
```

Isso permite criar consultas reutilizáveis sem repetir a mesma lógica em várias Views.