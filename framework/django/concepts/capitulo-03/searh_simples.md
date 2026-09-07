# Django — Busca com PostgreSQL no CinePost

## Objetivo

Depois de migrar o CinePost de SQLite para PostgreSQL, começamos a usar recursos de:

```text
Full-Text Search
```

O objetivo é permitir que o usuário pesquise filmes usando texto.

Exemplo:

```text
terror
```

e o CinePost procurar em:

```text
título
comentário principal
tags
```

---

# 1. Ativando recursos do PostgreSQL

No:

```text
config/settings.py
```

adicionamos:

```python
"django.contrib.postgres",
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

    "django.contrib.postgres",

    "taggit",

    "filmes.apps.FilmesConfig",
]
```

---

# Para que serve `django.contrib.postgres`?

Ele disponibiliza recursos específicos do PostgreSQL dentro do Django.

Entre eles:

```text
SearchVector
SearchQuery
SearchRank
```

Nesta primeira parte usamos principalmente:

```python
SearchVector
```

---

# 2. Busca simples com `__search`

No shell:

```powershell
python manage.py shell
```

Importamos:

```python
from filmes.models import PostFilme
```

Podemos pesquisar:

```python
PostFilme.publicados.filter(
    titulo__search="terror"
)
```

---

# O que é `__search`?

É um lookup de pesquisa textual utilizando PostgreSQL.

Exemplo:

```python
titulo__search="batman"
```

significa aproximadamente:

```text
Pesquise "batman" no campo título
usando o mecanismo de busca textual
do PostgreSQL.
```

---

# `icontains` x `search`

Já conhecíamos:

```python
titulo__icontains="batman"
```

Mentalmente:

```text
O texto contém "batman"?
```

Agora temos:

```python
titulo__search="batman"
```

Mentalmente:

```text
Esse conteúdo corresponde à busca "batman"?
```

A diferença vai ficando mais importante quando começamos a usar vários campos e relevância.

---

# 3. Pesquisando em vários campos

Para pesquisar em mais de um campo utilizamos:

```python
SearchVector
```

Importamos:

```python
from django.contrib.postgres.search import SearchVector
```

Depois:

```python
PostFilme.publicados.annotate(
    search=SearchVector(
        "titulo",
        "comentario",
    )
).filter(
    search="terror"
)
```

---

# O que é `SearchVector`?

Ele monta uma área de pesquisa utilizando vários campos.

No CinePost:

```text
titulo
+
comentario
```

Então:

```python
SearchVector(
    "titulo",
    "comentario",
)
```

faz o PostgreSQL considerar os dois campos durante a busca.

---

# Exemplo

Post:

```text
Título:
O Iluminado

Comentário:
Um clássico do terror psicológico.
```

Mesmo que a palavra:

```text
terror
```

não esteja no título, ela pode ser encontrada no comentário principal.

---

# 4. O papel do `annotate()`

Usamos:

```python
.annotate(
    search=SearchVector(...)
)
```

O `annotate()` cria temporariamente uma informação calculada para cada resultado.

Neste caso:

```text
search
```

não é um campo real do Model.

Não existe:

```python
search = models....
```

Não precisa:

```powershell
python manage.py makemigrations
```

É calculado apenas naquela consulta.

---

# Mentalmente

```text
PostFilme
↓
annotate()
↓
cria search temporariamente
↓
titulo + comentario
↓
filter(search=query)
```

---

# 5. Criando o formulário de busca

No:

```text
filmes/forms.py
```

criamos:

```python
class BuscaForm(forms.Form):
    query = forms.CharField()
```

---

# Por que `forms.Form`?

Porque não estamos criando nem alterando um objeto do banco.

Só queremos receber:

```text
texto digitado pelo usuário
```

Então usamos:

```python
forms.Form
```

e não:

```python
forms.ModelForm
```

---

# Diferença

```text
ModelForm
→ ligado a um Model
→ cria ou altera registros
```

```text
Form
→ formulário comum
→ recebe e valida informações
```

---

# Campo `query`

```python
query = forms.CharField()
```

Representa algo parecido com:

```html
<input type="text" name="query">
```

O usuário pode digitar:

```text
terror
```

---

# 6. Criando a view da busca

No:

```text
filmes/views.py
```

importamos:

```python
from django.contrib.postgres.search import SearchVector
from .forms import BuscaForm
```

Criamos:

```python
def post_search(request):
    form = BuscaForm()
    query = None
    resultados = []

    if "query" in request.GET:
        form = BuscaForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]

            resultados = (
                PostFilme.publicados
                .annotate(
                    search=SearchVector(
                        "titulo",
                        "comentario",
                    )
                )
                .filter(search=query)
            )

    return render(
        request,
        "filmes/post/search.html",
        {
            "form": form,
            "query": query,
            "resultados": resultados,
        },
    )
```

---

# 7. Estado inicial da view

Começamos com:

```python
form = BuscaForm()
query = None
resultados = []
```

Isso representa:

```text
formulário pronto
pesquisa ainda não feita
nenhum resultado ainda
```

---

# 8. Por que usamos `request.GET`?

Temos:

```python
if "query" in request.GET:
```

Quando o usuário pesquisa:

```text
terror
```

a URL pode ficar:

```text
/filmes/search/?query=terror
```

Então:

```text
query=terror
```

fica visível na URL.

---

# Por que GET em vez de POST?

Busca normalmente usa:

```text
GET
```

porque a pesquisa não altera dados.

Além disso, a URL pode ser:

```text
copiada
compartilhada
salva nos favoritos
```

Exemplo:

```text
/filmes/search/?query=terror
```

---

# POST normalmente é usado para

```text
criar comentário
fazer cadastro
alterar registros
enviar dados que modificam o sistema
```

---

# 9. Validando o formulário

Recebemos:

```python
form = BuscaForm(request.GET)
```

Depois:

```python
if form.is_valid():
```

Se estiver válido:

```python
query = form.cleaned_data["query"]
```

---

# `cleaned_data`

O:

```python
form.cleaned_data
```

contém os dados já processados e validados pelo Django.

Exemplo:

```python
query = "terror"
```

---

# 10. Executando a pesquisa

Inicialmente usamos:

```python
resultados = (
    PostFilme.publicados
    .annotate(
        search=SearchVector(
            "titulo",
            "comentario",
        )
    )
    .filter(search=query)
)
```

Fluxo:

```text
usuário pesquisa
↓
query
↓
PostFilme.publicados
↓
SearchVector
↓
titulo + comentario
↓
PostgreSQL pesquisa
↓
resultados
```

---

# 11. Criando o template

Criamos:

```text
filmes/templates/filmes/post/search.html
```

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}Buscar filmes{% endblock %}

{% block content %}

<div class="container py-4">

    {% if query %}

        <h1 class="h3 mb-3">
            Resultados para "{{ query }}"
        </h1>

        <p class="text-secondary">
            Encontrados: {{ resultados.count }}
        </p>

        <div class="vstack gap-3">

            {% for post in resultados %}

                <div class="card bg-black border-secondary">

                    <div class="card-body">

                        <h2 class="h5">
                            <a
                                href="{{ post.get_absolute_url }}"
                                class="text-light text-decoration-none"
                            >
                                {{ post.titulo }}
                            </a>
                        </h2>

                        <p class="text-secondary mb-0">
                            {{ post.comentario|truncatewords:30 }}
                        </p>

                    </div>

                </div>

            {% empty %}

                <p class="text-secondary">
                    Nenhum resultado encontrado.
                </p>

            {% endfor %}

        </div>

        <div class="mt-4">

            <a
                href="{% url 'filmes:post_search' %}"
                class="btn btn-outline-light"
            >
                Pesquisar novamente
            </a>

        </div>

    {% else %}

        <h1 class="h3 mb-4">
            Buscar filmes
        </h1>

        <form method="get">

            <div class="mb-3">
                {{ form.query.label_tag }}
                {{ form.query }}
            </div>

            <button
                type="submit"
                class="btn btn-danger"
            >
                Pesquisar
            </button>

        </form>

    {% endif %}

</div>

{% endblock %}
```

---

# 12. O `{% if query %}`

Temos:

```django
{% if query %}
```

Se o usuário já pesquisou:

```text
query = "terror"
```

mostramos:

```text
resultados
```

Se ainda não pesquisou:

```text
query = None
```

mostramos:

```text
formulário
```

---

# 13. Mostrando resultados

Usamos:

```django
{% for post in resultados %}
```

para percorrer os posts encontrados.

---

# Quantidade encontrada

```django
{{ resultados.count }}
```

Exemplo:

```text
Encontrados: 4
```

---

# Resumindo o comentário

Usamos:

```django
{{ post.comentario|truncatewords:30 }}
```

Isso limita a descrição a:

```text
30 palavras
```

---

# 14. Criando a URL

No:

```text
filmes/urls.py
```

adicionamos:

```python
path(
    "search/",
    views.post_search,
    name="post_search",
),
```

Agora temos:

```text
/filmes/search/
```

---

# Fluxo da rota

```text
/filmes/search/
↓
post_search
↓
BuscaForm
↓
SearchVector
↓
PostgreSQL
↓
search.html
```

---

# 15. URL com pesquisa

Se o usuário digitar:

```text
terror
```

a URL pode virar:

```text
/filmes/search/?query=terror
```

Isso acontece porque usamos:

```html
<form method="get">
```

---

# 16. Problema encontrado: comentários

Pesquisamos:

```text
terror
```

e inicialmente nenhum resultado apareceu.

O motivo era importante.

No CinePost existem dois conceitos diferentes:

```text
PostFilme.comentario
```

e:

```text
Comentario.texto
```

---

# `PostFilme.comentario`

É a crítica/opinião principal do autor do post.

Exemplo:

```text
Interestelar é um excelente filme de ficção científica...
```

---

# `Comentario.texto`

É o comentário social feito por visitantes.

Exemplo:

```text
Eu adorei esse filme!
```

---

# Nossa busca inicial

Estava usando:

```python
SearchVector(
    "titulo",
    "comentario",
)
```

Então pesquisava em:

```text
✅ PostFilme.titulo

✅ PostFilme.comentario

❌ Comentario.texto
```

---

# Testando onde estava a palavra

No shell:

```python
from filmes.models import PostFilme
```

Testamos:

```python
PostFilme.publicados.filter(
    comentario__icontains="terror"
)
```

E para comentários sociais:

```python
from filmes.models import Comentario
```

```python
Comentario.objects.filter(
    texto__icontains="terror"
)
```

Assim conseguimos identificar onde a palavra estava realmente armazenada.

---

# Importante

Nunca confundir:

```text
PostFilme.comentario
```

com:

```text
Comentario.texto
```

Eles são coisas diferentes.

---

# 17. Adicionando busca por tags

Depois decidimos que uma pesquisa também deveria encontrar tags.

Exemplo:

```text
Post:
O Iluminado

Tags:
terror
suspense
psicológico
```

Mesmo que a palavra:

```text
terror
```

não esteja no título nem na crítica, pesquisar por:

```text
terror
```

deve encontrar o filme pela tag.

---

# Importando `Q`

No:

```text
views.py
```

adicionamos:

```python
from django.db.models import Q
```

---

# O que é `Q`?

`Q` permite criar condições mais complexas no ORM.

Principalmente:

```text
OU
E
NEGAÇÃO
```

---

# O operador `|`

Dentro de uma consulta:

```python
Q(...)
|
Q(...)
```

significa:

```text
OU
```

---

# Busca atualizada

Alteramos para:

```python
resultados = (
    PostFilme.publicados
    .annotate(
        search=SearchVector(
            "titulo",
            "comentario",
        )
    )
    .filter(
        Q(search=query)
        | Q(tags__name__icontains=query)
    )
    .distinct()
)
```

---

# Agora pesquisamos em

```text
titulo
+
comentario principal
+
tags
```

---

# Entendendo a condição

```python
Q(search=query)
```

significa:

```text
encontre no SearchVector
```

Ou seja:

```text
titulo ou comentario principal
```

Depois:

```python
Q(tags__name__icontains=query)
```

significa:

```text
encontre também no nome da tag
```

Juntamos:

```python
Q(search=query)
| Q(tags__name__icontains=query)
```

Mentalmente:

```text
Está no título/comentário?

OU

Está na tag?
```

Se qualquer condição for verdadeira:

```text
o post aparece
```

---

# 18. Por que usamos `icontains` na tag?

Para tags usamos:

```python
tags__name__icontains=query
```

Exemplo:

```text
Tag:
terror psicológico
```

Pesquisa:

```text
terror
```

pode encontrar essa tag.

---

# 19. Por que usamos `distinct()`?

Um `PostFilme` pode possuir várias tags.

Exemplo:

```text
O Iluminado
├── terror
├── suspense
└── psicológico
```

Como estamos fazendo uma consulta através de uma relação:

```text
ManyToMany
```

o banco pode produzir mais de uma linha relacionada ao mesmo post.

Então usamos:

```python
.distinct()
```

Isso significa:

```text
retorne cada PostFilme apenas uma vez
```

---

# 20. Busca atual do CinePost

Nossa busca atual funciona assim:

```text
Usuário pesquisa
↓
query
↓
PostFilme.publicados
↓
SearchVector
├── titulo
└── comentario principal
↓
OU
↓
tags
↓
distinct()
↓
resultados
```

---

# Exemplo completo

Imagine:

```text
Título:
O Iluminado

Comentário principal:
Um clássico dirigido por Stanley Kubrick.

Tags:
terror
suspense
```

Se pesquisar:

```text
terror
```

o filme aparece porque:

```text
tag = terror
```

Mesmo que `terror` não esteja:

```text
no título
nem
no comentário principal
```

---

# 21. Código atual da busca

A parte principal da view ficou conceitualmente assim:

```python
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

from .forms import BuscaForm


def post_search(request):
    form = BuscaForm()
    query = None
    resultados = []

    if "query" in request.GET:
        form = BuscaForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]

            resultados = (
                PostFilme.publicados
                .annotate(
                    search=SearchVector(
                        "titulo",
                        "comentario",
                    )
                )
                .filter(
                    Q(search=query)
                    | Q(tags__name__icontains=query)
                )
                .distinct()
            )

    return render(
        request,
        "filmes/post/search.html",
        {
            "form": form,
            "query": query,
            "resultados": resultados,
        },
    )
```

---

# 22. O que já conseguimos fazer?

A busca atual consegue procurar:

```text
✅ título

✅ comentário principal do post

✅ tags
```

Ainda não estamos pesquisando diretamente:

```text
❌ comentários sociais dos visitantes
```

Isso pode ser acrescentado depois se quisermos.

---

# 23. Ainda é uma busca básica

Apesar de já estar funcionando, ainda estamos no começo da parte de Full-Text Search.

Ainda existem conceitos mais avançados como:

```text
SearchQuery
SearchRank
pesos
stemming
idioma
similaridade
índices
```

---

# `SearchQuery`

Será usado para representar melhor a consulta do usuário.

Mentalmente:

```text
texto digitado
↓
SearchQuery
↓
consulta preparada para PostgreSQL
```

---

# `SearchRank`

Pode calcular:

```text
quão relevante é cada resultado
```

Exemplo:

```text
O Iluminado      0.92
Hereditário      0.81
Corra             0.72
```

Assim podemos ordenar:

```text
mais relevante
↓
menos relevante
```

---

# Pesos

Também poderemos definir que alguns campos são mais importantes.

Exemplo:

```text
Título
→ peso alto

Tags
→ peso alto

Comentário principal
→ peso médio

Comentários sociais
→ peso menor
```

Então encontrar uma palavra no título pode valer mais do que encontrá-la no meio de um texto enorme.

---

# Exemplo futuro

Pesquisa:

```text
terror
```

Poderíamos chegar a algo assim:

```text
1. Terror na Estrada
   palavra no título

2. O Iluminado
   tag terror

3. Corra
   palavra na crítica

4. Outro filme
   palavra apenas em comentário social
```

---

# 24. Resumo mental

```text
django.contrib.postgres
= recursos extras do PostgreSQL
```

```text
__search
= lookup de busca textual
```

```text
SearchVector
= junta campos para pesquisa
```

```text
annotate()
= cria informação temporária na QuerySet
```

```text
BuscaForm
= recebe o texto digitado
```

```text
request.GET
= recebe a pesquisa pela URL
```

```text
cleaned_data
= dados validados pelo formulário
```

```text
Q()
= cria condições mais complexas
```

```text
|
= OU
```

```text
tags__name__icontains
= busca pelo nome da tag
```

```text
distinct()
= remove resultados duplicados
```

---

# Fluxo completo atual

```text
Usuário abre:

/filmes/search/

↓
BuscaForm

↓
digita:

terror

↓
GET:

?query=terror

↓
post_search()

↓
form.is_valid()

↓
cleaned_data["query"]

↓
SearchVector
├── titulo
└── comentario

OU

tags

↓
PostgreSQL

↓
QuerySet resultados

↓
search.html

↓
usuário vê os filmes encontrados
```

---

# Principal aprendizado

Antes fazíamos buscas simples como:

```python
titulo__icontains="terror"
```

Agora começamos a construir uma busca baseada nos recursos do PostgreSQL:

```text
Django
↓
SearchVector
↓
PostgreSQL Full-Text Search
↓
resultados
```

E já conseguimos combinar isso com recursos normais do ORM:

```text
SearchVector
+
Q
+
ManyToMany
+
tags
+
distinct
```

A busca já funciona, mas ainda vamos melhorar a qualidade dos resultados com relevância, pesos e outros recursos avançados.