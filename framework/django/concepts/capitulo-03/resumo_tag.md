# Django Taggit no CinePost

## O que são tags?

Tags são palavras-chave usadas para categorizar conteúdos.

Exemplo:

```text
Corra
├── Terror
├── Suspense
└── Psicológico
```

Um post pode ter várias tags e uma mesma tag pode pertencer a vários posts.

Isso é uma relação:

```text
muitos-para-muitos
```

Exemplo:

```text
Corra ───── Terror
Nós ─────── Terror
```

---

# Instalando django-taggit

Instalamos:

```powershell
python -m pip install django-taggit==6.1.0
```

Depois adicionamos no `settings.py`:

```python
INSTALLED_APPS = [
    # Apps do Django...

    "taggit",

    "filmes.apps.FilmesConfig",
]
```

Boa prática:

```text
Apps do Django
↓
Apps de terceiros
↓
Apps do projeto
```

---

# Adicionando tags ao PostFilme

No `models.py`:

```python
from taggit.managers import TaggableManager
```

Dentro de `PostFilme`:

```python
tags = TaggableManager()
```

Isso adiciona ao post um gerenciador:

```python
post.tags
```

---

# Migrations

Depois de alterar o Model:

```powershell
python manage.py makemigrations filmes
python manage.py migrate
```

O `migrate` também cria as tabelas necessárias do `django-taggit`.

---

# Trabalhando com tags no Shell

Abrimos:

```powershell
python manage.py shell
```

Importamos:

```python
from filmes.models import PostFilme
```

Pegamos um post:

```python
post = PostFilme.objects.get(id=1)
```

ou:

```python
post = PostFilme.objects.first()
```

## Adicionar tags

```python
post.tags.add(
    "terror",
    "suspense",
    "psicologico",
)
```

Não é necessário usar:

```python
post.save()
```

depois.

## Ver tags

```python
post.tags.all()
```

## Remover uma tag

```python
post.tags.remove("terror")
```

## Remover todas

```python
post.tags.clear()
```

## Buscar posts por tag

```python
PostFilme.objects.filter(tags__name="terror")
```

O Django atravessa o relacionamento:

```text
PostFilme
↓
tags
↓
name
↓
terror
```

---

# Tags no Admin

Depois de adicionar:

```python
tags = TaggableManager()
```

o Django Admin passa a permitir adicionar e editar tags nos posts.

O `django-taggit` também possui seu próprio Model `Tag`.

---

# Mostrando tags no Template

Forma simples:

```django
{{ post.tags.all|join:", " }}
```

Exemplo:

```text
terror, suspense, drama
```

O filtro:

```django
|join:", "
```

funciona de forma parecida com o `join()` do Python.

---

# Filtrando posts por tag

Criamos uma nova URL:

```python
path(
    "tag/<slug:tag_slug>/",
    views.PostListView.as_view(),
    name="post_list_by_tag",
)
```

Exemplo:

```text
/filmes/tag/terror/
```

Nesse caso:

```python
tag_slug = "terror"
```

---

# Adaptando a ListView

Importamos o Model `Tag`:

```python
from taggit.models import Tag
```

Nossa `PostListView` passou a controlar o filtro:

```python
class PostListView(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "filmes/post/list.html"

    def get_queryset(self):
        posts = PostFilme.publicados.all()

        self.tag = None

        tag_slug = self.kwargs.get("tag_slug")

        if tag_slug:
            self.tag = get_object_or_404(
                Tag,
                slug=tag_slug,
            )

            posts = posts.filter(
                tags__in=[self.tag]
            )

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tag"] = self.tag

        return context
```

---

# get_queryset()

O método:

```python
get_queryset()
```

define quais objetos a `ListView` vai mostrar.

Sem tag:

```text
/filmes/
↓
todos os posts
```

Com tag:

```text
/filmes/tag/terror/
↓
somente posts de terror
```

---

# self.kwargs

Em uma Class-Based View, parâmetros capturados pela URL ficam em:

```python
self.kwargs
```

Usamos:

```python
tag_slug = self.kwargs.get("tag_slug")
```

Exemplo:

```text
/filmes/tag/terror/
```

gera:

```python
tag_slug = "terror"
```

---

# Buscando a Tag

Usamos:

```python
self.tag = get_object_or_404(
    Tag,
    slug=tag_slug,
)
```

Se a tag existir:

```text
continua normalmente
```

Se não existir:

```text
404
```

---

# Filtrando os posts

Usamos:

```python
posts = posts.filter(
    tags__in=[self.tag]
)
```

Isso significa:

> Traga apenas os posts que possuem essa tag.

Aqui estamos filtrando através de uma relação muitos-para-muitos.

---

# get_context_data()

Usamos:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context["tag"] = self.tag

    return context
```

Assim o template recebe:

```text
posts
tag
page_obj
```

---

# Tags clicáveis

Antes:

```django
{{ post.tags.all|join:", " }}
```

Agora usamos:

```django
{% for tag_item in post.tags.all %}

    <a
        href="{% url 'filmes:post_list_by_tag' tag_item.slug %}"
        class="badge rounded-pill text-bg-secondary text-decoration-none"
    >
        {{ tag_item.name }}
    </a>

{% empty %}

    <span class="text-secondary small">
        Sem tags
    </span>

{% endfor %}
```

Visualmente:

```text
Tags: [terror] [suspense] [drama]
```

Cada tag agora é clicável.

---

# Criando a URL pelo Template

Usamos:

```django
{% url 'filmes:post_list_by_tag' tag_item.slug %}
```

Se:

```python
tag_item.slug == "terror"
```

o Django gera:

```text
/filmes/tag/terror/
```

Se:

```python
tag_item.slug == "ficcao-cientifica"
```

gera:

```text
/filmes/tag/ficcao-cientifica/
```

---

# Mostrando o filtro ativo

No template:

```django
{% if tag %}

    <div class="alert alert-dark border-secondary">

        <span class="text-secondary">
            Filtrando por:
        </span>

        <span class="badge bg-danger">
            {{ tag.name }}
        </span>

        <a
            href="{% url 'filmes:post_list' %}"
            class="btn btn-outline-light btn-sm"
        >
            Limpar filtro
        </a>

    </div>

{% endif %}
```

Exemplo:

```text
Filtrando por: [terror]     Limpar filtro
```

O botão `Limpar filtro` volta para a lista completa.

---

# Paginação

Como continuamos utilizando `ListView`, usamos:

```django
{% include "filmes/pagination.html" with page=page_obj %}
```

Não usamos:

```django
page=posts
```

porque essa abordagem era da Function-Based View usada pelo livro.

---

# Contador de publicações

Isto:

```django
{{ posts|length }}
```

conta apenas os posts da página atual.

Com paginação, preferimos:

```django
{{ page_obj.paginator.count }}
```

Exemplo:

```text
20 posts no total
3 posts por página
```

`posts|length`:

```text
3
```

`page_obj.paginator.count`:

```text
20
```

---

# Fluxo completo

```text
Usuário entra em /filmes/
↓
PostListView
↓
mostra todos os posts
↓
cada post mostra suas tags
↓
usuário clica em "terror"
↓
/filmes/tag/terror/
↓
URL captura tag_slug="terror"
↓
PostListView.get_queryset()
↓
busca a Tag
↓
filtra PostFilme por tags__in
↓
template recebe posts + tag
↓
mostra somente posts daquela tag
↓
usuário pode clicar em "Limpar filtro"
↓
volta para /filmes/
```

---

# Principais comandos e conceitos

## Gerenciador de tags

```python
TaggableManager()
```

## Adicionar tags

```python
post.tags.add("terror")
```

## Listar tags

```python
post.tags.all()
```

## Remover uma tag

```python
post.tags.remove("terror")
```

## Remover todas

```python
post.tags.clear()
```

## Filtrar pela tag

```python
posts.filter(tags__in=[tag])
```

## Parâmetros da URL em CBV

```python
self.kwargs
```

## Definir objetos da ListView

```python
get_queryset()
```

## Enviar informações extras ao template

```python
get_context_data()
```

## Gerar URL da tag

```django
{% url 'filmes:post_list_by_tag' tag_item.slug %}
```

---

# Resumo mental

```text
django-taggit
↓
TaggableManager
↓
PostFilme possui tags
↓
Post ↔ Tag = muitos-para-muitos
↓
URL recebe tag_slug
↓
ListView recebe pelo self.kwargs
↓
get_queryset() filtra
↓
get_context_data() envia a tag
↓
Template mostra as tags como links
↓
Usuário consegue filtrar os posts
```