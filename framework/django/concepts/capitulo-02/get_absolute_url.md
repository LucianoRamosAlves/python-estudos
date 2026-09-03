# Django — `get_absolute_url()`

## O problema

Imagine que cada filme tenha sua própria página de detalhes:

```text
/filmes/1/
/filmes/2/
/filmes/3/
```

Temos apenas **uma rota geral**:

```python
path(
    "<int:id>/",
    views.post_detail,
    name="post_detail",
)
```

Mas cada `PostFilme` possui seu próprio `id`.

Exemplo:

```text
Interestelar → ID 5
Matrix       → ID 8
Batman       → ID 12
```

Logo, cada objeto possui uma URL diferente:

```text
Interestelar → /filmes/5/
Matrix       → /filmes/8/
Batman       → /filmes/12/
```

---

# Sem `get_absolute_url()`

Para criar um link para um filme, podemos fazer:

```django
<a href="{% url 'filmes:post_detail' post.id %}">
    {{ post.titulo }}
</a>
```

Isso funciona.

Porém, o template precisa saber:

```text
Qual é a rota?
→ filmes:post_detail

Qual parâmetro ela precisa?
→ post.id
```

Se precisarmos criar links para o `PostFilme` em vários lugares:

```text
Home
Busca
Perfil
Favoritos
Recomendações
Lista de posts
```

todos esses lugares precisam conhecer a forma de construir a URL.

---

# Com `get_absolute_url()`

Podemos ensinar o próprio `PostFilme` a descobrir sua URL principal.

No `models.py`:

```python
from django.urls import reverse
```

Dentro do model:

```python
def get_absolute_url(self):
    return reverse(
        "filmes:post_detail",
        args=[self.id],
    )
```

Agora podemos fazer:

```python
post.get_absolute_url()
```

Se:

```python
post.id == 5
```

o resultado será algo como:

```text
/filmes/5/
```

---

# Analogia

Imagine que cada `PostFilme` seja uma pessoa.

Sem `get_absolute_url()`, você precisa montar o endereço dela:

```text
Rua = /filmes/
Número = 5
```

Resultado:

```text
/filmes/5/
```

Com `get_absolute_url()`, você simplesmente pergunta:

> Qual é o seu endereço?

No Django:

```python
post.get_absolute_url()
```

O objeto responde:

```text
/filmes/5/
```

---

# Usando no Template

Antes:

```django
<a href="{% url 'filmes:post_detail' post.id %}">
    {{ post.titulo }}
</a>
```

Depois:

```django
<a href="{{ post.get_absolute_url }}">
    {{ post.titulo }}
</a>
```

Agora o template não precisa saber como construir a URL.

Ele apenas pergunta ao objeto:

```django
{{ post.get_absolute_url }}
```

---

# O que é `reverse()`?

O `reverse()` transforma o **nome de uma rota** em uma URL real.

Temos:

```python
app_name = "filmes"
```

E:

```python
path(
    "<int:id>/",
    views.post_detail,
    name="post_detail",
)
```

Então podemos fazer:

```python
reverse(
    "filmes:post_detail",
    args=[5],
)
```

O Django procura:

```text
filmes
↓
namespace

post_detail
↓
nome da rota
```

e usa:

```text
5
```

como `id`.

Resultado:

```text
/filmes/5/
```

---

# `reverse()` x `get_absolute_url()`

## `reverse()`

Pergunta:

> Tenho o nome de uma rota. Qual é a URL?

```python
reverse(
    "filmes:post_detail",
    args=[5],
)
```

Resultado:

```text
/filmes/5/
```

---

## `get_absolute_url()`

Pergunta:

> Tenho um objeto. Qual é a URL principal dele?

```python
post.get_absolute_url()
```

Resultado:

```text
/filmes/5/
```

O `get_absolute_url()` usa o `reverse()` para descobrir essa URL.

---

# O que acontece quando o usuário clica?

O `get_absolute_url()` NÃO busca o objeto no banco e NÃO executa a View.

Ele apenas gera o endereço:

```text
/filmes/5/
```

Depois que o usuário clica:

```text
Clique no filme
        ↓
/filmes/5/
        ↓
urls.py
        ↓
post_detail
        ↓
id = 5
        ↓
View
        ↓
ORM
        ↓
Banco
        ↓
PostFilme ID 5
        ↓
Template
        ↓
Página de detalhes
```

---

# Importante

`get_absolute_url()` não serve para qualquer link automaticamente.

Por exemplo:

```text
/dashboard/
/login/
/contato/
```

são páginas fixas.

Normalmente não precisamos de `get_absolute_url()` para elas.

Ele é especialmente útil quando temos **objetos individuais com páginas próprias**.

Exemplo:

```text
PostFilme 1 → /filmes/1/
PostFilme 2 → /filmes/2/
PostFilme 3 → /filmes/3/
```

---

# Também pode funcionar com slug

Hoje podemos usar:

```text
/filmes/5/
```

Mas futuramente podemos ter:

```text
/filmes/interestelar/
/filmes/matrix/
/filmes/batman/
```

A ideia continua igual.

Cada objeto conhece sua própria URL principal.

---

# Resumo

Sem `get_absolute_url()`:

```django
{% url 'filmes:post_detail' post.id %}
```

Precisamos informar:

```text
rota + parâmetro
```

Com `get_absolute_url()`:

```django
{{ post.get_absolute_url }}
```

Perguntamos diretamente ao objeto:

> Qual é sua URL?

---

# Para decorar

```python
reverse()
```

> Pega o nome de uma rota e gera a URL real.

```python
get_absolute_url()
```

> Faz o objeto saber qual é sua URL principal.

```django
{{ post.get_absolute_url }}
```

> Usa essa URL no template.

Fluxo:

```text
PostFilme ID 5
        ↓
get_absolute_url()
        ↓
reverse(
    "filmes:post_detail",
    args=[5]
)
        ↓
urls.py
        ↓
/filmes/5/
```

## Ideia principal

> **Em vez de cada parte do projeto precisar saber como montar a URL de um `PostFilme`, o próprio objeto sabe informar qual é sua URL principal.**