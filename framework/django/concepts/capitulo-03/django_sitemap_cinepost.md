# Django — Sitemap no CinePost

## O que é um Sitemap?

Um sitemap é um arquivo que lista as páginas importantes do site.

Normalmente ele fica em:

```text
/sitemap.xml
```

Exemplo:

```text
http://localhost:8000/sitemap.xml
```

Ele é usado principalmente por mecanismos de busca, como Google e Bing, para descobrir quais páginas existem no site.

Mentalmente:

```text
CinePost
↓
várias páginas de filmes
↓
sitemap.xml
↓
lista essas páginas
↓
Google/Bing conseguem encontrá-las
```

---

# Para que serve?

Imagine que o CinePost tenha:

```text
/filmes/2026/9/7/interestelar/
/filmes/2026/9/7/corra/
/filmes/2026/9/7/duna/
```

O sitemap informa:

```text
Estas páginas existem no meu site.
```

Isso ajuda mecanismos de busca a descobrir e indexar o conteúdo.

Importante:

```text
Sitemap ajuda na descoberta/indexação
```

mas não significa:

```text
Tenho sitemap
↓
vou ficar em primeiro lugar no Google
```

---

# O que existe dentro do Sitemap?

O Django pode gerar algo parecido com:

```xml
<url>
    <loc>
        http://localhost:8000/filmes/2026/9/7/interestelar/
    </loc>

    <lastmod>
        2026-09-07
    </lastmod>

    <changefreq>
        weekly
    </changefreq>

    <priority>
        0.9
    </priority>
</url>
```

---

## `loc`

É a URL da página.

Exemplo:

```text
http://localhost:8000/filmes/2026/9/7/interestelar/
```

---

## `lastmod`

Indica quando aquela página foi alterada pela última vez.

No CinePost usamos:

```python
atualizado_em
```

---

## `changefreq`

Indica aproximadamente com que frequência a página pode mudar.

Exemplo:

```text
weekly
```

Significa:

```text
aproximadamente semanalmente
```

Não obriga o Google a visitar a página toda semana.

---

## `priority`

É uma prioridade relativa dentro do próprio site.

Exemplo:

```python
priority = 0.9
```

Os valores podem ficar entre:

```text
0.0 e 1.0
```

Isso não representa ranking no Google.

---

# Estrutura que vamos criar

No CinePost teremos:

```text
config/
├── settings.py
└── urls.py

filmes/
├── models.py
├── views.py
├── urls.py
└── sitemaps.py
```

O novo arquivo será:

```text
filmes/sitemaps.py
```

---

# Passo 1 — Ativar `sites` e `sitemaps`

Abra:

```text
config/settings.py
```

Dentro de:

```python
INSTALLED_APPS
```

adicione:

```python
"django.contrib.sites",
"django.contrib.sitemaps",
```

Exemplo:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    "django.contrib.sites",
    "django.contrib.sitemaps",

    "django.contrib.staticfiles",

    "taggit",

    "filmes.apps.FilmesConfig",
]
```

Também adicione:

```python
SITE_ID = 1
```

---

# O que é `django.contrib.sites`?

O sitemap precisa gerar URLs completas.

Por exemplo:

```text
http://localhost:8000/filmes/...
```

Então o Django precisa saber qual é o domínio do site.

É para isso que usamos:

```python
django.contrib.sites
```

Ele guarda informações como:

```text
Nome:
CinePost

Domínio:
localhost:8000
```

---

# O que é `django.contrib.sitemaps`?

É a ferramenta do Django responsável por gerar o arquivo:

```text
sitemap.xml
```

Então:

```text
django.contrib.sites
→ sabe qual é o domínio

django.contrib.sitemaps
→ gera o sitemap
```

---

# O que é `SITE_ID = 1`?

O Django pode administrar mais de um site.

Cada registro possui um ID.

Quando colocamos:

```python
SITE_ID = 1
```

estamos dizendo:

```text
Use o Site de ID 1 como o site atual.
```

---

# Passo 2 — Criar as tabelas do `sites`

Depois de alterar o `settings.py`, rode:

```powershell
python manage.py migrate
```

Devem aparecer migrations semelhantes a:

```text
Applying sites.0001_initial... OK
Applying sites.0002_alter_domain_unique... OK
```

---

## Por que não usamos `makemigrations`?

Não alteramos nenhum Model nosso.

As migrations de:

```text
django.contrib.sites
```

já vêm prontas com o Django.

Então basta:

```powershell
python manage.py migrate
```

---

# Passo 3 — Criar `sitemaps.py`

Crie:

```text
filmes/sitemaps.py
```

Coloque:

```python
from django.contrib.sitemaps import Sitemap

from .models import PostFilme


class PostFilmeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return PostFilme.publicados.all()

    def lastmod(self, obj):
        return obj.atualizado_em
```

---

# Entendendo `Sitemap`

Importamos:

```python
from django.contrib.sitemaps import Sitemap
```

Depois criamos:

```python
class PostFilmeSitemap(Sitemap):
```

Estamos herdando uma classe pronta do Django.

É parecido com:

```python
class PostListView(ListView):
```

Ou seja:

```text
Sitemap
↓
estrutura pronta do Django

PostFilmeSitemap
↓
nossa configuração
```

---

# `changefreq`

```python
changefreq = "weekly"
```

Indica que as páginas podem ser atualizadas aproximadamente semanalmente.

---

# `priority`

```python
priority = 0.9
```

Define uma prioridade relativa das páginas desse sitemap.

---

# `items()`

A parte principal:

```python
def items(self):
    return PostFilme.publicados.all()
```

Esse método responde:

```text
Quais objetos devem entrar no sitemap?
```

No CinePost usamos:

```python
PostFilme.publicados.all()
```

Então:

```text
Post publicado
✅ entra

Rascunho
❌ não entra
```

---

# Como o Django descobre a URL?

Não precisamos escrever manualmente:

```text
/filmes/2026/9/7/interestelar/
```

O Django usa:

```python
get_absolute_url()
```

do nosso `PostFilme`.

Já tínhamos criado esse método anteriormente.

Mentalmente:

```text
PostFilme
↓
get_absolute_url()
↓
/filmes/2026/9/7/interestelar/
```

O sitemap reutiliza essa informação.

---

# Por que `get_absolute_url()` foi importante?

Antes usamos para coisas como:

```django
<a href="{{ post.get_absolute_url }}">
```

Agora ele também serve para o sitemap.

Então:

```text
get_absolute_url()
```

virou a URL oficial do objeto dentro do projeto.

---

# `lastmod()`

Criamos:

```python
def lastmod(self, obj):
    return obj.atualizado_em
```

`obj` representa cada `PostFilme`.

Exemplo:

```text
obj
↓
Interestelar
```

Então:

```python
obj.atualizado_em
```

retorna a última vez em que o post foi atualizado.

---

# Resultado de `sitemaps.py`

Nossa classe informa:

```text
Quais posts entram
↓
PostFilme.publicados

Qual URL usar
↓
get_absolute_url()

Última alteração
↓
atualizado_em

Frequência
↓
weekly

Prioridade
↓
0.9
```

---

# Passo 4 — Criar a URL do Sitemap

Agora abra:

```text
config/urls.py
```

Importe:

```python
from django.contrib.sitemaps.views import sitemap

from filmes.sitemaps import PostFilmeSitemap
```

Depois crie:

```python
sitemaps = {
    "posts": PostFilmeSitemap,
}
```

E dentro de:

```python
urlpatterns
```

adicione:

```python
path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",
),
```

Exemplo completo:

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from filmes.sitemaps import PostFilmeSitemap


sitemaps = {
    "posts": PostFilmeSitemap,
}


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "filmes/",
        include("filmes.urls"),
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

---

# O que é o dicionário `sitemaps`?

Criamos:

```python
sitemaps = {
    "posts": PostFilmeSitemap,
}
```

Hoje temos apenas um sitemap:

```text
posts
→ PostFilmeSitemap
```

Mas futuramente poderíamos ter:

```python
sitemaps = {
    "posts": PostFilmeSitemap,
    "categorias": CategoriaSitemap,
    "paginas": PaginaSitemap,
}
```

---

# O que a rota faz?

Esta rota:

```python
path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
)
```

cria:

```text
/sitemap.xml
```

O fluxo fica:

```text
/sitemap.xml
↓
view sitemap do Django
↓
dicionário sitemaps
↓
PostFilmeSitemap
↓
items()
↓
posts publicados
↓
XML
```

---

# Passo 5 — Testar o Sitemap

Inicie o servidor:

```powershell
python manage.py runserver
```

Abra:

```text
http://127.0.0.1:8000/sitemap.xml
```

Você deve ver um arquivo XML.

Exemplo:

```xml
<urlset>

    <url>

        <loc>
            http://example.com/filmes/2026/9/7/interestelar/
        </loc>

        <lastmod>
            2026-09-07
        </lastmod>

        <changefreq>
            weekly
        </changefreq>

        <priority>
            0.9
        </priority>

    </url>

</urlset>
```

---

# Por que aparece `example.com`?

Quando ativamos:

```python
django.contrib.sites
```

o Django cria um Site padrão:

```text
example.com
```

Por isso inicialmente o sitemap pode gerar:

```text
http://example.com/filmes/...
```

Isso é normal.

Precisamos editar esse Site.

---

# Passo 6 — Configurar o domínio no Admin

Abra:

```text
http://127.0.0.1:8000/admin/sites/site/
```

Clique em:

```text
example.com
```

Você encontrará:

```text
Nome do domínio
Nome para exibição
```

Troque para:

```text
Nome do domínio:
localhost:8000
```

E:

```text
Nome para exibição:
CinePost
```

Depois clique em:

```text
SALVAR
```

---

# Importante sobre o domínio

Use:

```text
localhost:8000
```

Não use:

```text
http://localhost:8000
```

E não precisa colocar:

```text
http://
```

O Django cuida do protocolo quando monta a URL.

---

# Passo 7 — Testar novamente

Abra novamente:

```text
http://127.0.0.1:8000/sitemap.xml
```

Agora as URLs devem aparecer semelhantes a:

```text
http://localhost:8000/filmes/2026/9/7/interestelar/
```

---

# Como a URL completa é criada?

Nosso `get_absolute_url()` retorna algo como:

```text
/filmes/2026/9/7/interestelar/
```

O `django.contrib.sites` fornece:

```text
localhost:8000
```

O Django junta:

```text
localhost:8000
+
/filmes/2026/9/7/interestelar/
```

Resultado:

```text
http://localhost:8000/filmes/2026/9/7/interestelar/
```

---

# Quando o site estiver online

Hoje usamos:

```text
localhost:8000
```

porque estamos em desenvolvimento.

Quando o CinePost estiver publicado, podemos trocar por algo como:

```text
cinepost.com.br
```

Então o sitemap poderá gerar:

```text
https://cinepost.com.br/filmes/...
```

---

# Fluxo completo do Sitemap

```text
PostFilme
↓
PostFilme.publicados
↓
PostFilmeSitemap.items()
↓
pega todos os posts publicados
↓
get_absolute_url()
↓
descobre a URL de cada post
↓
lastmod()
↓
pega atualizado_em
↓
django.contrib.sites
↓
adiciona o domínio
↓
django.contrib.sitemaps
↓
gera sitemap.xml
```

---

# Arquivos envolvidos

## `config/settings.py`

Responsável por ativar:

```python
"django.contrib.sites"
"django.contrib.sitemaps"
```

e definir:

```python
SITE_ID = 1
```

---

## `filmes/sitemaps.py`

Responsável por definir:

```text
quais objetos entram
frequência
prioridade
última modificação
```

---

## `PostFilme.get_absolute_url()`

Responsável por informar:

```text
qual é a URL de cada PostFilme
```

---

## `config/urls.py`

Responsável por criar:

```text
/sitemap.xml
```

---

## Django Admin → Sites

Responsável por configurar:

```text
qual é o domínio atual
```

---

# Código final de `sitemaps.py`

```python
from django.contrib.sitemaps import Sitemap

from .models import PostFilme


class PostFilmeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return PostFilme.publicados.all()

    def lastmod(self, obj):
        return obj.atualizado_em
```

---

# Código principal no `settings.py`

```python
SITE_ID = 1


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",

    "taggit",

    "filmes.apps.FilmesConfig",
]
```

---

# Código principal no `config/urls.py`

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from filmes.sitemaps import PostFilmeSitemap


sitemaps = {
    "posts": PostFilmeSitemap,
}


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "filmes/",
        include("filmes.urls"),
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

---

# Comandos usados

Depois de ativar `sites`:

```powershell
python manage.py migrate
```

Para executar o projeto:

```powershell
python manage.py runserver
```

---

# Resumo mental

```text
Sitemap
= mapa das URLs para mecanismos de busca

django.contrib.sites
= sabe qual é o domínio

django.contrib.sitemaps
= gera o XML

PostFilmeSitemap
= define quais posts entram

items()
= retorna os posts publicados

get_absolute_url()
= fornece a URL

lastmod()
= fornece a última alteração

config/urls.py
= cria /sitemap.xml
```

---

# Principal aprendizado

O sitemap reaproveita várias coisas que já construímos anteriormente:

```text
PostFilme
↓
manager publicados
↓
get_absolute_url()
↓
atualizado_em
↓
Sitemap
```

Ou seja, o Django pega estruturas que já existem no projeto e usa essas informações para gerar automaticamente:

```text
/sitemap.xml
```

sem precisarmos cadastrar cada URL manualmente.