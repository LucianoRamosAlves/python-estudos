# Django — URL amigável com data + slug

## Objetivo

Antes, a página de detalhes de um post usava somente o ID:

```text
/filmes/5/
```

Agora queremos uma URL mais descritiva:

```text
/filmes/2026/9/3/interestelar/
```

A URL passa a usar:

```text
ano
+
mês
+
dia
+
slug
```

---

# 1. Preparar o slug no Model

No `models.py`, o campo `slug` pode ficar assim:

```python
slug = models.SlugField(
    max_length=250,
    unique_for_date="publicado_em",
)
```

O:

```python
unique_for_date="publicado_em"
```

significa:

> Na mesma data de publicação, dois posts não devem ter o mesmo slug.

Exemplo permitido:

```text
03/09/2026 → interestelar
04/09/2026 → interestelar
```

Datas diferentes.

Exemplo não permitido pela validação do Django:

```text
03/09/2026 → interestelar
03/09/2026 → interestelar
```

Mesma data + mesmo slug.

---

# 2. Criar a migration

Como o Model foi alterado:

```bash
python manage.py makemigrations filmes
```

Depois:

```bash
python manage.py migrate
```

Mesmo que `unique_for_date` não crie uma restrição direta no banco, a migration registra o estado atual do Model.

---

# 3. Alterar a URL

Antes:

```python
path(
    "<int:id>/",
    views.post_detail,
    name="post_detail",
)
```

Agora:

```python
path(
    "<int:year>/<int:month>/<int:day>/<slug:post>/",
    views.post_detail,
    name="post_detail",
)
```

A URL agora pode ser:

```text
/filmes/2026/9/3/interestelar/
```

O Django extrai:

```python
year = 2026
month = 9
day = 3
post = "interestelar"
```

---

# 4. Alterar a View

Antes, a View recebia:

```python
def post_detail(request, id):
```

Agora recebe:

```python
def post_detail(request, year, month, day, post):
```

No CinePost:

```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        PostFilme.publicados,
        slug=post,
        publicado_em__year=year,
        publicado_em__month=month,
        publicado_em__day=day,
    )

    return render(
        request,
        "filmes/post/detail.html",
        {"post": post},
    )
```

Agora o post é encontrado usando:

```text
slug
+
ano
+
mês
+
dia
```

em vez de usar apenas:

```text
id
```

---

# 5. Alterar o `get_absolute_url()`

Antes:

```python
def get_absolute_url(self):
    return reverse(
        "filmes:post_detail",
        args=[self.id],
    )
```

Isso funcionava para:

```text
/filmes/5/
```

Agora precisamos passar:

```text
ano
mês
dia
slug
```

Então:

```python
def get_absolute_url(self):
    return reverse(
        "filmes:post_detail",
        args=[
            self.publicado_em.year,
            self.publicado_em.month,
            self.publicado_em.day,
            self.slug,
        ],
    )
```

Se o objeto possuir:

```text
publicado_em = 03/09/2026
slug = interestelar
```

o resultado será:

```text
/filmes/2026/9/3/interestelar/
```

---

# Alternativa com `kwargs`

Também podemos escrever:

```python
def get_absolute_url(self):
    return reverse(
        "filmes:post_detail",
        kwargs={
            "year": self.publicado_em.year,
            "month": self.publicado_em.month,
            "day": self.publicado_em.day,
            "post": self.slug,
        },
    )
```

Essa forma deixa mais explícito qual valor pertence a cada parâmetro.

---

# 6. O Template continua simples

Como já usamos:

```django
<a href="{{ post.get_absolute_url }}">
    {{ post.titulo }}
</a>
```

não precisamos colocar manualmente:

```text
ano
mês
dia
slug
```

no template.

O próprio `PostFilme` informa sua URL.

---

# Fluxo completo

Imagine:

```text
Título: Interestelar
Slug: interestelar
Data: 03/09/2026
```

O objeto faz:

```python
post.get_absolute_url()
```

↓

```python
reverse(
    "filmes:post_detail",
    ...
)
```

↓

```text
/filmes/2026/9/3/interestelar/
```

Quando o usuário clica:

```text
/filmes/2026/9/3/interestelar/
↓
urls.py
↓
year = 2026
month = 9
day = 3
post = "interestelar"
↓
post_detail()
↓
ORM procura slug + data
↓
PostFilme correto
↓
detail.html
```

---

# Antes x Depois

## Antes

```text
/filmes/5/
```

Busca:

```python
id=5
```

## Depois

```text
/filmes/2026/9/3/interestelar/
```

Busca:

```python
slug="interestelar"
publicado_em__year=2026
publicado_em__month=9
publicado_em__day=3
```

---

# Ordem para decorar

```text
1. Slug no Model
      ↓
2. makemigrations
      ↓
3. migrate
      ↓
4. URL com data + slug
      ↓
5. View recebe data + slug
      ↓
6. get_absolute_url() gera nova URL
      ↓
7. Template usa post.get_absolute_url
```

## Ideia principal

> O `slug` deixa a URL mais legível.

> A data + slug identificam qual post deve ser aberto.

> O `get_absolute_url()` faz cada `PostFilme` saber gerar sua própria URL.