# Django — RSS Feed no CinePost

## O que é RSS?

RSS é uma forma de disponibilizar as novidades de um site em um formato que outros programas conseguem ler.

Pense assim:

```text
CinePost publica algo novo
↓
RSS é atualizado
↓
um leitor RSS percebe
↓
o usuário vê a nova publicação
```

É parecido com:

```text
YouTube
→ inscritos acompanham vídeos novos

Podcast
→ app acompanha episódios novos

RSS
→ leitor acompanha posts novos
```

---

# Para que serve?

O RSS serve para que usuários ou aplicativos acompanhem conteúdos recentes de um site sem precisar abrir o site toda hora.

No CinePost, ele pode mostrar os últimos posts publicados.

Exemplo:

```text
CinePost

Últimos posts:
- Interestelar
- Corra
- Duna
- Matrix
- Oppenheimer
```

---

# Por que parece código no navegador?

Porque o RSS normalmente é gerado em XML.

Exemplo:

```xml
<rss>
    <channel>

        <title>CinePost</title>

        <item>
            <title>Interestelar</title>
            <link>...</link>
        </item>

    </channel>
</rss>
```

Isso não foi feito para ficar bonito no navegador.

Ele foi feito para ser lido por programas chamados:

```text
leitores RSS
```

Esses programas transformam o XML em uma interface mais amigável.

---

# RSS não é para deficiência visual

RSS não foi criado especificamente para pessoas com deficiência visual.

Ele pode ser usado por ferramentas acessíveis, mas a finalidade principal é:

```text
acompanhar novidades de sites
```

---

# Diferença entre Sitemap e RSS

## Sitemap

```text
sitemap.xml
→ mecanismos de busca
→ Google/Bing
→ descobrir páginas do site
```

## RSS

```text
feed/
→ usuários e aplicativos
→ acompanhar conteúdo recente
```

Resumo:

```text
Sitemap
= mapa das páginas do site

RSS
= lista de novidades do site
```

---

# O Django já possui suporte a RSS

O Django possui um framework pronto chamado:

```python
django.contrib.syndication
```

Por isso não precisamos criar o XML manualmente.

---

# Passo 1 — Criar `feeds.py`

Dentro do app `filmes`, criamos:

```text
filmes/feeds.py
```

A estrutura fica:

```text
filmes/
├── admin.py
├── feeds.py
├── forms.py
├── models.py
├── sitemaps.py
├── urls.py
└── views.py
```

---

# Código do Feed

Dentro de:

```text
filmes/feeds.py
```

criamos:

```python
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import PostFilme


class UltimosPostsFeed(Feed):
    title = "CinePost"

    link = reverse_lazy(
        "filmes:post_list"
    )

    description = "Últimas publicações do CinePost."

    def items(self):
        return (
            PostFilme.publicados
            .order_by("-publicado_em")[:5]
        )

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords(
            item.comentario,
            30,
        )

    def item_pubdate(self, item):
        return item.publicado_em
```

---

# Entendendo o código

## `Feed`

Importamos:

```python
from django.contrib.syndication.views import Feed
```

Depois criamos:

```python
class UltimosPostsFeed(Feed):
```

Estamos herdando uma classe pronta do Django.

É parecido com:

```python
class PostListView(ListView):
```

ou:

```python
class PostFilmeSitemap(Sitemap):
```

Mentalmente:

```text
Feed
↓
estrutura pronta do Django
↓
UltimosPostsFeed
↓
configuramos para o CinePost
```

---

# `title`

```python
title = "CinePost"
```

Define o nome do feed.

Um leitor RSS pode mostrar:

```text
CinePost
```

---

# `description`

```python
description = "Últimas publicações do CinePost."
```

É uma descrição do conteúdo do feed.

---

# `link`

Usamos:

```python
link = reverse_lazy(
    "filmes:post_list"
)
```

Isso aponta para a página principal dos posts.

---

# O que é `reverse_lazy()`?

Já conhecemos:

```python
reverse()
```

Ele transforma o nome de uma rota em URL.

Exemplo:

```python
reverse("filmes:post_list")
```

pode gerar:

```text
/filmes/
```

`reverse_lazy()` faz algo parecido, mas resolve a URL somente quando ela for necessária.

Mentalmente:

```text
reverse()
→ resolve agora

reverse_lazy()
→ resolve depois, quando precisar
```

É útil em atributos de classes.

---

# `items()`

Criamos:

```python
def items(self):
    return (
        PostFilme.publicados
        .order_by("-publicado_em")[:5]
    )
```

Isso responde:

```text
Quais posts devem entrar no RSS?
```

No CinePost:

```text
somente posts publicados
↓
mais recentes primeiro
↓
máximo de 5
```

---

# `order_by("-publicado_em")`

O `-` significa ordem decrescente.

Então:

```text
mais recente
↓
mais antigo
```

---

# `[:5]`

Limita o resultado aos cinco primeiros posts.

```python
[:5]
```

significa:

```text
pegue apenas 5
```

---

# `item_title()`

```python
def item_title(self, item):
    return item.titulo
```

Define o título de cada item do RSS.

Exemplo:

```text
Interestelar
```

---

# `item_description()`

```python
def item_description(self, item):
    return truncatewords(
        item.comentario,
        30,
    )
```

Pega o comentário principal do post e limita a 30 palavras.

Isso evita colocar textos muito grandes no feed.

---

# `truncatewords`

Usamos:

```python
truncatewords(
    item.comentario,
    30,
)
```

Isso transforma um texto grande em uma versão menor.

Exemplo:

```text
texto original:
100 palavras
```

vira:

```text
texto no RSS:
30 palavras
```

---

# `item_pubdate()`

```python
def item_pubdate(self, item):
    return item.publicado_em
```

Define a data de publicação do item.

---

# URL de cada post

O Django pode usar:

```python
get_absolute_url()
```

do nosso `PostFilme`.

Então:

```text
PostFilme
↓
get_absolute_url()
↓
URL oficial
↓
RSS
```

Mais uma vez reaproveitamos algo que já criamos anteriormente.

---

# Passo 2 — Criar a URL do Feed

Abra:

```text
filmes/urls.py
```

Importe:

```python
from .feeds import UltimosPostsFeed
```

Depois adicione:

```python
path(
    "feed/",
    UltimosPostsFeed(),
    name="post_feed",
),
```

---

# Exemplo de `urls.py`

```python
from django.urls import path

from . import views
from .feeds import UltimosPostsFeed


app_name = "filmes"


urlpatterns = [
    path(
        "",
        views.PostListView.as_view(),
        name="post_list",
    ),

    path(
        "tag/<slug:tag_slug>/",
        views.PostListView.as_view(),
        name="post_list_by_tag",
    ),

    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),

    path(
        "<int:post_id>/recomendar/",
        views.recomendar_post,
        name="recomendar_post",
    ),

    path(
        "<int:post_id>/comentar/",
        views.comentar_post,
        name="comentar_post",
    ),

    path(
        "feed/",
        UltimosPostsFeed(),
        name="post_feed",
    ),
]
```

---

# O que essa rota faz?

```python
path(
    "feed/",
    UltimosPostsFeed(),
    name="post_feed",
)
```

cria:

```text
/filmes/feed/
```

O fluxo fica:

```text
/filmes/feed/
↓
UltimosPostsFeed()
↓
items()
↓
últimos 5 posts
↓
Django gera XML RSS
```

---

# Passo 3 — Testar o RSS

Inicie o servidor:

```powershell
python manage.py runserver
```

Abra:

```text
http://127.0.0.1:8000/filmes/feed/
```

Você deve ver algo parecido com XML.

Exemplo:

```xml
<rss version="2.0">

    <channel>

        <title>CinePost</title>

        <description>
            Últimas publicações do CinePost.
        </description>

        <item>

            <title>
                Interestelar
            </title>

            <description>
                ...
            </description>

            <link>
                ...
            </link>

        </item>

    </channel>

</rss>
```

Isso é normal.

---

# Por que fica feio?

Porque o navegador está mostrando o XML bruto.

O RSS foi pensado para ser consumido por:

```text
leitores RSS
```

Esses programas transformam os dados em algo como:

```text
CinePost

Interestelar
Publicado hoje

Corra
Publicado ontem

Duna
Publicado há 2 dias
```

---

# Passo 4 — Criar link para o RSS

No `base.html`, podemos colocar:

```django
<a
    href="{% url 'filmes:post_feed' %}"
    class="btn btn-outline-danger btn-sm"
>
    Assinar RSS
</a>
```

Ou:

```django
<a
    href="{% url 'filmes:post_feed' %}"
    class="text-danger text-decoration-none"
>
    Assinar o feed RSS
</a>
```

---

# O que acontece ao clicar?

```text
usuário clica
↓
/filmes/feed/
↓
UltimosPostsFeed
↓
busca os últimos posts
↓
gera RSS
```

---

# Precisa instalar alguma biblioteca?

Para essa versão do CinePost:

```text
NÃO
```

O suporte a RSS já vem com o Django através de:

```python
django.contrib.syndication
```

Então não precisamos executar:

```powershell
pip install ...
```

para o RSS básico.

---

# E o Markdown do livro?

O livro usa Markdown dentro do RSS.

Como decidimos não usar Markdown no CinePost agora, usamos:

```python
truncatewords
```

diretamente no:

```python
item.comentario
```

Então nosso feed ficou mais simples.

---

# Fluxo completo

```text
PostFilme
↓
PostFilme.publicados
↓
order_by("-publicado_em")
↓
[:5]
↓
UltimosPostsFeed
↓
item_title()
↓
item_description()
↓
item_pubdate()
↓
get_absolute_url()
↓
/filmes/feed/
↓
Django gera XML RSS
↓
leitor RSS pode consumir
```

---

# Arquivos envolvidos

## `filmes/feeds.py`

Define:

```text
o conteúdo do RSS
```

---

## `filmes/urls.py`

Cria:

```text
/filmes/feed/
```

---

## `PostFilme`

Fornece:

```text
título
comentário
data
URL
```

---

# Conceitos principais

## `Feed`

```python
class UltimosPostsFeed(Feed):
```

Cria um feed usando o framework do Django.

---

## `items()`

```python
def items(self):
```

Define quais objetos entram no feed.

---

## `item_title()`

```python
def item_title(self, item):
```

Define o título de cada publicação.

---

## `item_description()`

```python
def item_description(self, item):
```

Define o resumo de cada publicação.

---

## `item_pubdate()`

```python
def item_pubdate(self, item):
```

Define a data de publicação.

---

## `reverse_lazy()`

```python
reverse_lazy("filmes:post_list")
```

Resolve a URL de forma tardia.

---

# Resumo mental

```text
RSS
= canal de novidades do site

Feed
= classe pronta do Django

items()
= quais posts entram

item_title()
= título

item_description()
= resumo

item_pubdate()
= data

feed/
= endereço do RSS
```

---

# Principal aprendizado

O RSS mostra que o Django não serve apenas para gerar páginas HTML.

Ele também pode gerar dados para outros programas consumirem.

```text
Django
↓
não gera somente HTML
↓
também pode gerar XML
↓
outros aplicativos podem usar esses dados
```

No CinePost:

```text
posts recentes
↓
RSS
↓
outros programas conseguem acompanhar
```