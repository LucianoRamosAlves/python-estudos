# Django — Full-Text Search no CinePost

# PARTE 1 — Da busca simples até relevância, idioma e pesos

## 1. Objetivo

Depois de migrar o CinePost de:

```text
SQLite
```

para:

```text
PostgreSQL
```

começamos a construir uma busca mais avançada.

O objetivo foi sair de uma pesquisa simples como:

```python
titulo__icontains="terror"
```

e chegar a uma busca capaz de:

```text
pesquisar em vários campos
entender melhor as palavras
considerar o idioma português
calcular relevância
dar mais importância ao título
pesquisar pelas tags
```

Mais tarde acrescentamos também tolerância a erros de digitação.

---

# 2. Ativando os recursos do PostgreSQL

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

# 3. Para que serve `django.contrib.postgres`?

É uma parte do Django que disponibiliza funcionalidades específicas do PostgreSQL.

Entre elas:

```text
SearchVector
SearchQuery
SearchRank
TrigramSimilarity
```

Esses recursos não fazem parte da busca comum que utilizávamos com SQLite.

---

# 4. Primeira busca com `__search`

Podemos abrir o shell:

```powershell
python manage.py shell
```

Importar:

```python
from filmes.models import PostFilme
```

E pesquisar:

```python
PostFilme.publicados.filter(
    titulo__search="terror"
)
```

---

# 5. `icontains` x `search`

Já conhecíamos:

```python
titulo__icontains="terror"
```

Isso pergunta basicamente:

```text
O texto contém a sequência "terror"?
```

Já:

```python
titulo__search="terror"
```

utiliza o mecanismo de Full-Text Search do PostgreSQL.

Mentalmente:

```text
icontains
→ comparação simples de texto
```

```text
search
→ mecanismo de pesquisa textual do PostgreSQL
```

---

# 6. Pesquisando em vários campos

Queríamos pesquisar não apenas no título, mas também no comentário principal do post.

Para isso usamos:

```python
SearchVector
```

Importamos:

```python
from django.contrib.postgres.search import SearchVector
```

Exemplo:

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

# 7. O que é `SearchVector`?

Ele cria uma representação pesquisável utilizando um ou mais campos.

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

significa:

```text
Use título e comentário principal
como conteúdo da pesquisa.
```

---

# 8. Exemplo

Post:

```text
Título:
O Iluminado

Comentário:
Um dos maiores filmes de terror psicológico.
```

Se pesquisarmos:

```text
terror
```

o post pode ser encontrado mesmo que:

```text
terror
```

não esteja no título.

---

# 9. O papel do `annotate()`

Usamos:

```python
.annotate(
    search=SearchVector(...)
)
```

O `annotate()` acrescenta uma informação calculada temporariamente aos objetos da QuerySet.

Nesse caso criamos:

```text
search
```

Mas:

```text
search NÃO é um campo do Model.
```

Não precisamos executar:

```powershell
python manage.py makemigrations
```

---

# 10. Analogia com algo que já aprendemos

Anteriormente usamos:

```python
.annotate(
    total_comentarios=Count(...)
)
```

para criar:

```text
total_comentarios
```

temporariamente.

Agora fazemos algo parecido:

```python
.annotate(
    search=SearchVector(...)
)
```

---

# 11. Criando o formulário de busca

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

# 12. Por que usamos `forms.Form`?

Porque a busca não cria nem altera registros.

Queremos apenas receber:

```text
texto digitado pelo usuário
```

Portanto usamos:

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
→ recebe e valida informações
→ não precisa estar ligado a Model
```

---

# 13. O campo `query`

Criamos:

```python
query = forms.CharField()
```

Esse campo corresponde conceitualmente a:

```html
<input type="text" name="query" />
```

O usuário pode digitar:

```text
terror psicológico
```

---

# 14. Criando a view de pesquisa

No:

```text
filmes/views.py
```

criamos:

```python
def post_search(request):
```

A estrutura inicial foi:

```python
def post_search(request):
    form = BuscaForm()
    query = None
    resultados = []

    if "query" in request.GET:
        form = BuscaForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]

            resultados = ...

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

# 15. Estado inicial

Começamos com:

```python
form = BuscaForm()
query = None
resultados = []
```

Isso representa:

```text
formulário disponível
pesquisa ainda não realizada
nenhum resultado ainda
```

---

# 16. Por que usamos `GET`?

Verificamos:

```python
if "query" in request.GET:
```

Nosso formulário usa:

```html
<form method="get"></form>
```

Quando o usuário pesquisa:

```text
terror
```

a URL fica parecida com:

```text
/filmes/search/?query=terror
```

---

# 17. Vantagem do GET para pesquisa

Essa URL pode ser:

```text
copiada
compartilhada
salva nos favoritos
```

Pesquisa normalmente não altera dados.

Por isso:

```text
GET
```

é apropriado.

---

# 18. GET x POST

```text
GET
→ consultar informações
→ pesquisas
→ filtros
```

```text
POST
→ enviar informações que alteram o sistema
→ comentários
→ cadastros
→ formulários de criação
```

---

# 19. Validando o formulário

Recebemos:

```python
form = BuscaForm(request.GET)
```

Depois:

```python
if form.is_valid():
```

E pegamos:

```python
query = form.cleaned_data["query"]
```

---

# 20. `cleaned_data`

É onde o Django disponibiliza os dados já processados e validados pelo formulário.

Exemplo:

```python
query = "terror"
```

---

# 21. Criando o template

Criamos:

```text
filmes/templates/filmes/post/search.html
```

A ideia principal:

```django
{% if query %}
```

Se já existe uma pesquisa:

```text
mostramos resultados
```

Caso contrário:

```text
mostramos formulário
```

---

# 22. Percorrendo resultados

Usamos:

```django
{% for post in resultados %}
```

E mostramos:

```django
{{ post.titulo }}
```

junto com:

```django
{{ post.comentario|truncatewords:30 }}
```

---

# 23. `truncatewords`

```django
{{ post.comentario|truncatewords:30 }}
```

limita o texto exibido a aproximadamente:

```text
30 palavras
```

Assim a tela de busca não mostra críticas gigantes.

---

# 24. Criando a URL da busca

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

# 25. Fluxo básico

```text
/filmes/search/
↓
post_search()
↓
BuscaForm
↓
usuário digita
↓
GET
↓
SearchVector
↓
PostgreSQL
↓
resultados
↓
search.html
```

---

# 26. Comentário principal x comentários dos visitantes

Descobrimos um detalhe importante no nosso projeto.

Existem:

```text
PostFilme.comentario
```

e:

```text
Comentario.texto
```

Eles são coisas diferentes.

---

# `PostFilme.comentario`

É a crítica/opinião principal do post.

Exemplo:

```text
Um excelente filme de terror psicológico...
```

---

# `Comentario.texto`

É um comentário social feito por um visitante.

Exemplo:

```text
Gostei muito desse filme!
```

---

# Nossa busca atual

Pesquisa:

```text
✅ PostFilme.titulo
✅ PostFilme.comentario
```

Mas ainda não pesquisa:

```text
❌ Comentario.texto
```

---

# 27. Testando onde uma palavra estava

Podemos usar:

```python
PostFilme.publicados.filter(
    comentario__icontains="terror"
)
```

E para comentários sociais:

```python
Comentario.objects.filter(
    texto__icontains="terror"
)
```

Isso nos ajudou a entender a diferença entre os dois Models.

---

# 28. Adicionando tags à pesquisa

Também queremos encontrar filmes através das tags.

Exemplo:

```text
Título:
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

não esteja no título nem na crítica, queremos encontrar o post.

---

# 29. Usando `Q`

Importamos:

```python
from django.db.models import Q
```

E usamos:

```python
Q(search=query)
| Q(tags__name__icontains=query)
```

---

# 30. O que significa `|`?

Dentro de condições `Q`:

```python
|
```

significa:

```text
OU
```

Então:

```python
Q(search=query)
| Q(tags__name__icontains=query)
```

significa:

```text
Encontre no texto

OU

encontre nas tags
```

---

# 31. Buscando pelas tags

```python
tags__name__icontains=query
```

significa:

```text
acesse tags
↓
pegue o nome
↓
verifique se contém o texto pesquisado
```

---

# 32. Por que usamos `distinct()`?

`PostFilme` e tags possuem relação:

```text
ManyToMany
```

Um post pode ter:

```text
terror
suspense
psicológico
```

Uma consulta envolvendo ManyToMany pode produzir repetição do mesmo post.

Então usamos:

```python
.distinct()
```

Que significa:

```text
retorne cada post apenas uma vez
```

---

# 33. Stemming

Depois avançamos para:

```text
stemming
```

Stemming é o processo de reduzir palavras relacionadas a uma forma linguística comum.

Exemplo conceitual:

```text
filme
filmes
```

ou:

```text
musical
musicais
```

O mecanismo de busca tenta trabalhar com a raiz lexical das palavras para melhorar as correspondências.

---

# 34. Stop words

O PostgreSQL também consegue ignorar palavras extremamente comuns que normalmente possuem pouca importância para a busca.

Em português, exemplos poderiam ser:

```text
o
a
de
do
da
em
```

Por exemplo:

```text
filme de terror
```

o termo:

```text
de
```

normalmente não é importante para determinar o resultado.

---

# 35. `SearchQuery`

Passamos a usar:

```python
SearchQuery
```

Import:

```python
from django.contrib.postgres.search import SearchQuery
```

Depois:

```python
search_query = SearchQuery(
    query,
    config="portuguese",
)
```

---

# 36. Para que serve `SearchQuery`?

Transforma o texto digitado pelo usuário em uma consulta apropriada para o mecanismo Full-Text Search do PostgreSQL.

Mentalmente:

```text
"filmes de terror"
↓
SearchQuery
↓
análise linguística
↓
consulta PostgreSQL
```

---

# 37. Configuração em português

Como nosso conteúdo está em português, usamos:

```python
config="portuguese"
```

Tanto no:

```python
SearchVector
```

quanto no:

```python
SearchQuery
```

Exemplo:

```python
search_vector = SearchVector(
    "titulo",
    "comentario",
    config="portuguese",
)
```

E:

```python
search_query = SearchQuery(
    query,
    config="portuguese",
)
```

---

# 38. Por que isso é importante?

Porque stemming e stop words dependem do idioma.

O livro trabalha principalmente com inglês.

Nosso CinePost está em português.

Portanto usamos:

```text
portuguese
```

---

# 39. Ranking de resultados

Também queríamos responder:

```text
Qual resultado é mais relevante?
```

Para isso usamos:

```python
SearchRank
```

Import:

```python
from django.contrib.postgres.search import SearchRank
```

---

# 40. Criando o rank

```python
rank=SearchRank(
    search_vector,
    search_query,
)
```

Exemplo conceitual:

```text
O Iluminado
rank = 0.81

Corra
rank = 0.62

Outro filme
rank = 0.25
```

---

# 41. `rank` também é temporário

Assim como:

```text
search
```

o:

```text
rank
```

é criado pelo `annotate()`.

Não é campo do banco.

Não fazemos migration.

---

# 42. Ordenando pela relevância

Usamos:

```python
.order_by("-rank")
```

O sinal:

```text
-
```

significa ordem decrescente.

Então:

```text
maior rank
↓
menor rank
```

---

# 43. Pesos na pesquisa

Depois decidimos que encontrar uma palavra no título deveria valer mais do que encontrar no comentário.

Criamos:

```python
search_vector = (
    SearchVector(
        "titulo",
        weight="A",
        config="portuguese",
    )
    + SearchVector(
        "comentario",
        weight="B",
        config="portuguese",
    )
)
```

---

# 44. Pesos do PostgreSQL

Os pesos disponíveis são:

```text
A → maior peso
B → peso intermediário
C → peso menor
D → menor peso
```

O livro apresenta os valores padrão aproximadamente como:

```text
A → 1.0
B → 0.4
C → 0.2
D → 0.1
```

---

# 45. No CinePost

Definimos:

```text
Título
→ A
→ mais importante
```

```text
Comentário principal
→ B
→ menos importante que o título
```

---

# 46. Exemplo

Pesquisa:

```text
terror
```

Post A:

```text
Título:
Terror na Floresta
```

Post B:

```text
Título:
A Floresta

Comentário:
Um excelente filme de terror...
```

O Post A tende a receber rank maior porque a correspondência ocorreu no:

```text
título
```

que possui:

```text
weight="A"
```

---

# 47. Testando o rank

Temporariamente podemos colocar no template:

```django
{{ post.rank }}
```

Por exemplo:

```django
<p>
    Rank: {{ post.rank }}
</p>
```

Assim conseguimos visualizar a pontuação calculada.

Depois do teste podemos remover.

---

# 48. Código da busca antes dos trigramas

A lógica ficou semelhante a:

```python
search_vector = (
    SearchVector(
        "titulo",
        weight="A",
        config="portuguese",
    )
    + SearchVector(
        "comentario",
        weight="B",
        config="portuguese",
    )
)

search_query = SearchQuery(
    query,
    config="portuguese",
)

resultados = (
    PostFilme.publicados
    .annotate(
        search=search_vector,
        rank=SearchRank(
            search_vector,
            search_query,
        ),
    )
    .filter(
        Q(search=search_query)
        | Q(tags__name__icontains=query)
    )
    .order_by("-rank")
    .distinct()
)
```

---

# 49. Até aqui nossa busca conseguia

```text
✅ pesquisar no título

✅ pesquisar no comentário principal

✅ pesquisar nas tags

✅ usar regras do português

✅ aplicar stemming

✅ remover stop words conforme a configuração linguística

✅ calcular relevância

✅ dar mais importância ao título

✅ ordenar pelos melhores resultados
```

---

# PARTE 2 — Trigramas, erros de digitação e versão final

# 50. Problema restante

Mesmo com Full-Text Search, existe outro problema muito comum:

```text
erros de digitação
```

Exemplo:

O banco possui:

```text
Batman
```

Mas o usuário pesquisa:

```text
Batmam
```

Queremos ainda ter chance de encontrar:

```text
Batman
```

---

# 51. O que é trigram?

Um trigram é um grupo de três caracteres consecutivos.

Exemplo simplificado:

```text
batman
```

pode ser dividido em partes semelhantes a:

```text
bat
atm
tma
man
```

O PostgreSQL consegue comparar quantos desses grupos duas palavras possuem em comum.

---

# 52. Trigram Similarity

Isso permite medir:

```text
quanto duas strings são parecidas
```

Exemplo:

```text
Batman
Batmam
```

Possuem bastante semelhança.

Enquanto:

```text
Batman
Interestelar
```

possuem muito menos.

---

# 53. Extensão `pg_trgm`

O PostgreSQL precisa de uma extensão chamada:

```text
pg_trgm
```

para trabalhar com trigramas.

---

# 54. Criando uma migration vazia

Executamos:

```powershell
python manage.py makemigrations --name=trigram_ext --empty filmes
```

Isso criou uma migration parecida com:

```text
filmes/migrations/0005_trigram_ext.py
```

O número pode variar.

---

# 55. O que significa `--empty`?

Normalmente:

```powershell
python manage.py makemigrations
```

analisa mudanças nos Models.

Mas dessa vez:

```text
não alteramos nenhum Model
```

Queremos criar uma migration manual.

Por isso usamos:

```text
--empty
```

Mentalmente:

```text
makemigrations normal
→ Django detecta alterações
→ Django cria operações
```

```text
makemigrations --empty
→ Django cria arquivo vazio
→ nós definimos a operação
```

---

# 56. Editando a migration

Adicionamos:

```python
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations
```

E:

```python
operations = [
    TrigramExtension(),
]
```

Exemplo:

```python
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("filmes", "MIGRATION_ANTERIOR"),
    ]

    operations = [
        TrigramExtension(),
    ]
```

---

# 57. O que `TrigramExtension()` faz?

Ele manda o PostgreSQL habilitar:

```text
pg_trgm
```

Por baixo dos panos, corresponde à ideia de executar:

```sql
CREATE EXTENSION pg_trgm;
```

---

# 58. Aplicando a migration

Executamos:

```powershell
python manage.py migrate filmes
```

Resultado esperado:

```text
Applying filmes.XXXX_trigram_ext... OK
```

---

# 59. Por que usar migration para isso?

Porque agora a necessidade da extensão passa a fazer parte do histórico do projeto.

Se criarmos outro banco PostgreSQL e executarmos:

```powershell
python manage.py migrate
```

o Django também poderá instalar a extensão necessária.

Isso combina com a ideia que já aprendemos:

```text
migrations
= histórico de construção do banco
```

---

# 60. `TrigramSimilarity`

Depois importamos:

```python
from django.contrib.postgres.search import TrigramSimilarity
```

Exemplo:

```python
resultados = (
    PostFilme.publicados
    .annotate(
        similarity=TrigramSimilarity(
            "titulo",
            query,
        )
    )
    .filter(
        similarity__gt=0.1
    )
    .order_by(
        "-similarity"
    )
)
```

---

# 61. O que é `similarity`?

Criamos outra informação temporária com `annotate()`:

```text
similarity
```

Ela representa:

```text
quanto o título se parece com o texto pesquisado
```

Exemplo conceitual:

```text
Título: Batman
Pesquisa: Batmam

similarity = 0.65
```

Outro:

```text
Título: Titanic
Pesquisa: Batmam

similarity = 0.03
```

---

# 62. Filtrando por similaridade

Usamos:

```python
.filter(
    similarity__gt=0.1
)
```

`gt` significa:

```text
greater than
```

ou:

```text
maior que
```

Então:

```python
similarity__gt=0.1
```

significa:

```text
similaridade maior que 0.1
```

---

# 63. Ordenando por similaridade

```python
.order_by("-similarity")
```

faz:

```text
mais parecido
↓
menos parecido
```

---

# 64. Testando erro de digitação

Se existir:

```text
Batman
```

podemos tentar:

```text
Batmam
```

ou:

```text
Batmn
```

e verificar se o filme ainda aparece.

---

# 65. Vendo a similaridade no template

Durante os testes podemos adicionar:

```django
<p>
    Similaridade: {{ post.similarity }}
</p>
```

Depois podemos remover.

---

# 66. Juntando tudo

Não queríamos perder:

```text
Full-Text Search
tags
ranking
pesos
```

só para usar trigramas.

Então combinamos todas as técnicas.

---

# 67. Imports finais

No:

```text
filmes/views.py
```

ficamos com:

```python
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)

from django.db.models import Q
```

---

# 68. Versão final da view

```python
def post_search(request):
    form = BuscaForm()
    query = None
    resultados = []

    if "query" in request.GET:
        form = BuscaForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["query"]

            search_vector = (
                SearchVector(
                    "titulo",
                    weight="A",
                    config="portuguese",
                )
                + SearchVector(
                    "comentario",
                    weight="B",
                    config="portuguese",
                )
            )

            search_query = SearchQuery(
                query,
                config="portuguese",
            )

            resultados = (
                PostFilme.publicados
                .annotate(
                    search=search_vector,

                    rank=SearchRank(
                        search_vector,
                        search_query,
                    ),

                    similarity=TrigramSimilarity(
                        "titulo",
                        query,
                    ),
                )
                .filter(
                    Q(search=search_query)
                    | Q(tags__name__icontains=query)
                    | Q(similarity__gt=0.1)
                )
                .order_by(
                    "-rank",
                    "-similarity",
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

# 69. Entendendo a versão final

Primeiro:

```python
SearchVector(
    "titulo",
    weight="A",
)
```

significa:

```text
pesquise no título
e dê bastante importância a ele
```

---

Depois:

```python
SearchVector(
    "comentario",
    weight="B",
)
```

significa:

```text
pesquise também na crítica
mas com peso menor
```

---

Depois:

```python
SearchQuery(
    query,
    config="portuguese",
)
```

significa:

```text
prepare o texto pesquisado
usando regras linguísticas do português
```

---

Depois:

```python
SearchRank(
    search_vector,
    search_query,
)
```

significa:

```text
calcule a relevância do post
```

---

Depois:

```python
TrigramSimilarity(
    "titulo",
    query,
)
```

significa:

```text
calcule quanto o título se parece
com o texto digitado
```

---

# 70. Condições finais

Temos:

```python
.filter(
    Q(search=search_query)
    | Q(tags__name__icontains=query)
    | Q(similarity__gt=0.1)
)
```

Isso significa:

```text
Encontre se:

corresponde ao Full-Text Search

OU

possui uma tag correspondente

OU

o título é parecido o suficiente
```

---

# 71. Visualmente

```text
Pesquisa do usuário
        ↓
┌──────────────────────────────┐
│ Full-Text Search             │
│                              │
│ título → peso A              │
│ comentário → peso B          │
│ idioma → português           │
│ stemming                     │
│ stop words                   │
│ ranking                      │
└──────────────────────────────┘
        │
        ├────────── OU ──────────► tags
        │
        └────────── OU ──────────► trigram
                                    │
                                    ▼
                              erros de digitação

        ↓
     resultados
        ↓
   distinct()
        ↓
mais relevantes primeiro
```

---

# 72. Ordem dos resultados

Usamos:

```python
.order_by(
    "-rank",
    "-similarity",
)
```

Primeiro o Django/PostgreSQL considera:

```text
rank
```

Depois, em caso de necessidade:

```text
similarity
```

---

# 73. `distinct()` novamente

Como ainda estamos usando:

```python
tags__name
```

através de uma relação ManyToMany, mantemos:

```python
.distinct()
```

para evitar repetição de posts.

---

# 74. O que a busca final consegue fazer?

Atualmente:

```text
✅ pesquisar pelo título

✅ pesquisar pelo comentário principal

✅ pesquisar pelas tags

✅ utilizar PostgreSQL Full-Text Search

✅ analisar português

✅ aplicar stemming

✅ lidar com stop words

✅ calcular relevância

✅ dar peso maior ao título

✅ ordenar os melhores resultados

✅ tolerar determinados erros de digitação

✅ evitar duplicação causada pelas tags
```

---

# 75. O que ela ainda NÃO pesquisa?

Por enquanto:

```text
❌ comentários sociais dos visitantes
```

Ou seja:

```python
Comentario.texto
```

não faz parte do nosso `SearchVector`.

Isso pode ser acrescentado futuramente se fizer sentido.

---

# 76. Sobre o limite `0.1`

Utilizamos:

```python
similarity__gt=0.1
```

Esse valor é relativamente permissivo.

Quanto menor:

```text
mais resultados parecidos aparecem
```

Quanto maior:

```text
mais exigente fica a comparação
```

Podemos ajustar futuramente conforme testarmos dados reais.

---

# 77. Comparação de todas as etapas

## Busca mais simples

```python
titulo__icontains=query
```

```text
texto contém?
```

---

## Full-Text Search básico

```python
titulo__search=query
```

```text
pesquisa textual PostgreSQL
```

---

## SearchVector

```python
SearchVector(
    "titulo",
    "comentario",
)
```

```text
pesquisa em vários campos
```

---

## SearchQuery

```python
SearchQuery(
    query,
    config="portuguese",
)
```

```text
interpreta a consulta
```

---

## SearchRank

```python
SearchRank(...)
```

```text
mede relevância
```

---

## Weight

```python
weight="A"
weight="B"
```

```text
define importância dos campos
```

---

## Tags

```python
Q(tags__name__icontains=query)
```

```text
pesquisa pelas tags
```

---

## Trigram

```python
TrigramSimilarity(...)
```

```text
encontra strings parecidas
e ajuda com erros de digitação
```

---

# 78. Principais conceitos aprendidos

```text
django.contrib.postgres
= recursos específicos do PostgreSQL
```

```text
SearchVector
= cria conteúdo pesquisável
```

```text
SearchQuery
= representa a consulta do usuário
```

```text
SearchRank
= calcula relevância
```

```text
weight
= define importância dos campos
```

```text
config="portuguese"
= usa regras linguísticas do português
```

```text
stemming
= normaliza palavras relacionadas
```

```text
stop words
= palavras muito comuns que podem ser ignoradas
```

```text
Q()
= combina condições
```

```text
|
= OU
```

```text
distinct()
= elimina registros repetidos
```

```text
pg_trgm
= extensão PostgreSQL para trigramas
```

```text
TrigramSimilarity
= mede semelhança entre strings
```

```text
--empty
= cria migration vazia para operação manual
```

---

# 79. Fluxo final completo

```text
Usuário acessa:

/filmes/search/

↓
BuscaForm

↓
digita:

"terror"

↓
GET

?query=terror

↓
post_search()

↓
form.is_valid()

↓
cleaned_data["query"]

↓
SearchQuery
config="portuguese"

↓
SearchVector

├── titulo
│   └── weight A
│
└── comentario
    └── weight B

↓
SearchRank

↓
ao mesmo tempo verificamos:

tags

e

TrigramSimilarity no título

↓
Q(... OR ... OR ...)

↓
PostgreSQL

↓
distinct()

↓
order_by("-rank", "-similarity")

↓
resultados

↓
search.html
```

---

# 80. Principal aprendizado desta seção

Começamos com algo muito simples:

```python
titulo__icontains="terror"
```

e chegamos a uma busca muito mais completa:

```text
Full-Text Search
+
idioma português
+
stemming
+
stop words
+
vários campos
+
pesos
+
ranking
+
tags
+
trigram similarity
```

Tudo isso continua sendo utilizado através do:

```text
Django ORM
```

Sem escrever manualmente as consultas SQL complexas do PostgreSQL.

O fluxo continua:

```text
nosso Python
↓
Django ORM
↓
PostgreSQL
↓
mecanismo avançado de busca
```

Essa foi a grande evolução da busca do CinePost.
