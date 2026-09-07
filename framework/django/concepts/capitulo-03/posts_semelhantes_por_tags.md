# Django — Recomendação de Posts Semelhantes por Tags

## Objetivo

Depois de implementar as tags no CinePost, podemos utilizá-las para encontrar posts parecidos.

A ideia é recomendar outros posts que possuam tags em comum com o post que o usuário está lendo.

Exemplo:

```text
Interestelar

Tags:
- ficcao-cientifica
- espaco
- drama
```

Outros posts:

```text
Gravidade
- espaco
- drama

Perdido em Marte
- ficcao-cientifica
- espaco

Titanic
- drama

Corra
- terror
```

Os mais semelhantes seriam:

```text
1. Gravidade
   → 2 tags em comum

2. Perdido em Marte
   → 2 tags em comum

3. Titanic
   → 1 tag em comum
```

`Corra` não aparece porque não possui nenhuma tag em comum.

---

# Etapas da recomendação

Para encontrar posts semelhantes fazemos:

```text
1. Pegamos as tags do post atual
↓
2. Procuramos outros posts com essas tags
↓
3. Excluímos o próprio post
↓
4. Contamos quantas tags cada post tem em comum
↓
5. Ordenamos pelos mais semelhantes
↓
6. Em caso de empate, mostramos o mais recente
↓
7. Limitamos a quantidade de recomendações
```

---

# 1. Importando Count

No `views.py`:

```python
from django.db.models import Count
```

`Count` é uma função de agregação do Django ORM.

Ela permite fazer contagens diretamente durante uma consulta.

Algumas funções de agregação do Django são:

```text
Count → quantidade
Avg   → média
Max   → maior valor
Min   → menor valor
```

Nesta funcionalidade usamos:

```python
Count("tags")
```

para contar quantas tags estão relacionadas com cada resultado da consulta.

---

# 2. Pegando as tags do post atual

Dentro da `post_detail`:

```python
post_tags_ids = post.tags.values_list(
    "id",
    flat=True,
)
```

Suponha que o post tenha as tags:

```text
ID 2 → ficcao-cientifica
ID 5 → espaco
ID 8 → drama
```

O resultado será semelhante a:

```python
[2, 5, 8]
```

---

## O que é `values_list()`?

`values_list()` permite buscar somente determinados campos.

Por exemplo:

```python
post.tags.values_list("id")
```

poderia retornar:

```python
[(2,), (5,), (8,)]
```

São tuplas.

Com:

```python
flat=True
```

obtemos valores simples:

```python
[2, 5, 8]
```

Então:

```python
post.tags.values_list("id", flat=True)
```

significa:

> Pegue somente os IDs das tags desse post.

---

# 3. Buscando posts que possuem essas tags

Depois usamos:

```python
PostFilme.publicados.filter(
    tags__in=post_tags_ids
)
```

O `__in` significa:

> O valor deve estar dentro dessa lista de valores.

Se:

```python
post_tags_ids = [2, 5, 8]
```

o Django procura posts que possuam alguma dessas tags.

Conceitualmente:

```text
PostFilme
↓
tags
↓
tag está dentro de [2, 5, 8]
```

---

# 4. Excluindo o próprio post

Existe um problema.

O post atual possui exatamente essas tags.

Então ele também seria encontrado pela consulta.

Para não recomendar o próprio post:

```python
.exclude(id=post.id)
```

Exemplo:

```text
Estou lendo Interestelar

Recomendações:

❌ Interestelar
✅ Gravidade
✅ Perdido em Marte
```

Usamos:

```python
.exclude(id=post.id)
```

para retirar `Interestelar` dos resultados.

---

# 5. Contando as tags em comum

Agora usamos:

```python
.annotate(
    mesmas_tags=Count("tags")
)
```

Essa é a parte mais importante.

`annotate()` adiciona uma informação calculada temporariamente aos objetos retornados pelo QuerySet.

Exemplo:

```text
Gravidade
mesmas_tags = 2

Perdido em Marte
mesmas_tags = 2

Titanic
mesmas_tags = 1
```

---

# O que é `annotate()`?

Imagine que nosso Model possui:

```text
PostFilme

titulo
comentario
nota
publicado_em
...
```

Durante essa consulta fazemos:

```python
.annotate(
    mesmas_tags=Count("tags")
)
```

Temporariamente os resultados passam a ter:

```text
PostFilme

titulo
comentario
nota
publicado_em

mesmas_tags ← valor calculado
```

`mesmas_tags` NÃO vira um campo do Model.

Não cria migration.

Não cria coluna no banco.

Existe apenas durante aquele QuerySet.

---

# 6. Ordenando pelos mais semelhantes

Depois usamos:

```python
.order_by(
    "-mesmas_tags",
    "-publicado_em",
)
```

Primeiro:

```python
"-mesmas_tags"
```

significa:

> Maior quantidade de tags em comum primeiro.

O `-` indica ordem decrescente.

Exemplo:

```text
3 tags
2 tags
2 tags
1 tag
```

---

## Critério de desempate

Depois temos:

```python
"-publicado_em"
```

Se dois posts tiverem a mesma quantidade de tags em comum, o mais recente aparece primeiro.

Exemplo:

```text
Post A
2 tags em comum
Publicado ontem

Post B
2 tags em comum
Publicado há 1 mês
```

Resultado:

```text
1. Post A
2. Post B
```

---

# 7. Limitando a quantidade

No final usamos:

```python
[:4]
```

Isso limita o QuerySet aos primeiros 4 resultados.

Então mostramos no máximo:

```text
4 posts semelhantes
```

---

# QuerySet completo

O código fica:

```python
post_tags_ids = post.tags.values_list(
    "id",
    flat=True,
)

posts_similares = (
    PostFilme.publicados
    .filter(tags__in=post_tags_ids)
    .exclude(id=post.id)
    .annotate(
        mesmas_tags=Count("tags")
    )
    .order_by(
        "-mesmas_tags",
        "-publicado_em",
    )[:4]
)
```

Leia o código assim:

```text
PostFilme publicados
↓
que tenham alguma tag em comum
↓
exclua o post atual
↓
conte quantas tags possuem em comum
↓
ordene por mais tags em comum
↓
em empate, coloque o mais recente primeiro
↓
pegue somente os 4 primeiros
```

---

# 8. `post_detail` completa

No `views.py`:

```python
from django.db.models import Count
```

Na `post_detail`:

```python
def post_detail(request, year, month, day, post):

    post = get_object_or_404(
        PostFilme.publicados,
        slug=post,
        publicado_em__year=year,
        publicado_em__month=month,
        publicado_em__day=day,
    )

    comentarios = post.comentarios.filter(
        ativo=True
    )

    form = ComentarioForm()

    # IDs das tags do post atual
    post_tags_ids = post.tags.values_list(
        "id",
        flat=True,
    )

    # Posts semelhantes
    posts_similares = (
        PostFilme.publicados
        .filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(
            mesmas_tags=Count("tags")
        )
        .order_by(
            "-mesmas_tags",
            "-publicado_em",
        )[:4]
    )

    return render(
        request,
        "filmes/post/detail.html",
        {
            "post": post,
            "comentarios": comentarios,
            "form": form,
            "posts_similares": posts_similares,
        },
    )
```

---

# 9. Enviando os posts para o template

No `render()` adicionamos:

```python
"posts_similares": posts_similares,
```

Agora o `detail.html` pode acessar:

```django
posts_similares
```

---

# 10. Mostrando os posts semelhantes

No `detail.html`:

```django
<h2>Posts semelhantes</h2>

{% for post_similar in posts_similares %}

    <p>
        <a href="{{ post_similar.get_absolute_url }}">
            {{ post_similar.titulo }}
        </a>
    </p>

{% empty %}

    <p>
        Ainda não existem posts semelhantes.
    </p>

{% endfor %}
```

Usamos:

```django
post_similar
```

em vez de `post` para não confundir com o post atual.

---

# 11. Usando Bootstrap

No CinePost transformamos os posts semelhantes em cards.

Estrutura básica:

```django
<section class="mb-5">

    <h2 class="h3 mb-3">
        Posts semelhantes
    </h2>

    <div class="row g-3">

        {% for post_similar in posts_similares %}

            <div class="col-12 col-md-6">

                <article class="card h-100 bg-dark border-secondary">

                    <div class="card-body d-flex flex-column">

                        <h3 class="h5">

                            <a
                                href="{{ post_similar.get_absolute_url }}"
                                class="text-decoration-none text-light"
                            >
                                {{ post_similar.titulo }}
                            </a>

                        </h3>

                        <p class="text-secondary small">
                            Publicado em {{ post_similar.publicado_em }}
                        </p>

                        <a
                            href="{{ post_similar.get_absolute_url }}"
                            class="btn btn-outline-danger btn-sm mt-auto align-self-start"
                        >
                            Ver publicação
                        </a>

                    </div>

                </article>

            </div>

        {% empty %}

            <div class="col-12">

                <div class="alert alert-dark border-secondary">
                    Ainda não existem posts semelhantes.
                </div>

            </div>

        {% endfor %}

    </div>

</section>
```

---

# 12. Mostrando as tags dos posts semelhantes

Também podemos mostrar as tags dentro dos cards:

```django
{% for tag_item in post_similar.tags.all %}

    <span class="badge rounded-pill text-bg-secondary">
        {{ tag_item.name }}
    </span>

{% endfor %}
```

Isso é interessante porque são justamente as tags que estão sendo usadas para calcular a semelhança.

Exemplo:

```text
Gravidade

[espaco] [drama]

Ver publicação
```

---

# Fluxo completo da funcionalidade

```text
Usuário abre Interestelar
↓
post_detail()
↓
busca Interestelar
↓
pega os IDs das tags
↓
[2, 5, 8]
↓
procura outros posts com essas tags
↓
exclui Interestelar
↓
Count("tags")
↓
calcula quantidade de tags em comum
↓
annotate(mesmas_tags=...)
↓
ordena por mesmas_tags
↓
em empate, ordena por publicado_em
↓
limita aos 4 primeiros
↓
envia posts_similares para detail.html
↓
template mostra recomendações
```

---

# Conceitos novos

## `values_list()`

Retorna somente determinados valores do QuerySet.

```python
post.tags.values_list("id")
```

---

## `flat=True`

Transforma:

```python
[(1,), (2,), (3,)]
```

em:

```python
[1, 2, 3]
```

---

## `__in`

Verifica se um valor está dentro de uma coleção.

```python
tags__in=post_tags_ids
```

---

## `exclude()`

Remove resultados do QuerySet.

```python
.exclude(id=post.id)
```

---

## `Count()`

Realiza uma contagem através do ORM.

```python
Count("tags")
```

---

## `annotate()`

Adiciona informações calculadas temporariamente aos objetos do QuerySet.

```python
.annotate(
    mesmas_tags=Count("tags")
)
```

Não altera o Model e não exige migration.

---

## `order_by("-campo")`

O `-` significa ordem decrescente.

```python
.order_by("-mesmas_tags")
```

Resultado:

```text
3
2
1
```

---

## Slicing

```python
[:4]
```

limita o resultado aos 4 primeiros objetos.

---

# Resumo mental

```text
Tags do post atual
↓
values_list()
↓
IDs das tags
↓
filter(tags__in=...)
↓
outros posts relacionados
↓
exclude()
↓
retira o próprio post
↓
annotate() + Count()
↓
calcula a semelhança
↓
order_by()
↓
mais semelhantes primeiro
↓
[:4]
↓
quatro recomendações
```

---

# Principal aprendizado

Antes utilizamos tags apenas para:

```text
categorizar
↓
clicar
↓
filtrar posts
```

Agora usamos essas mesmas relações para gerar uma funcionalidade mais inteligente:

```text
tags em comum
↓
QuerySet
↓
contagem
↓
ranking
↓
recomendação de conteúdo
```

Essa funcionalidade é chamada de:

**Recomendação de posts semelhantes por tags.**