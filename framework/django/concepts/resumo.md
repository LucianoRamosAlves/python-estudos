# Django — Capítulo 1: Construindo uma aplicação

> Resumo adaptado para o projeto **CinePost**.

---

# 1. Visão geral do Django

Django é um framework web escrito em Python.

Ele fornece várias ferramentas prontas para construir aplicações web, como:

- sistema de URLs;
- Views;
- Templates;
- ORM;
- migrations;
- autenticação;
- painel administrativo;
- formulários;
- segurança;
- arquivos estáticos.

O fluxo básico de uma aplicação Django é:

```text
Usuário
   ↓
URL
   ↓
View
   ↓
Model / ORM
   ↓
Banco de dados
   ↓
Template
   ↓
HttpResponse
   ↓
Navegador
```

---

# 2. Arquitetura MTV

Django utiliza uma arquitetura chamada **MTV**:

```text
M = Model
T = Template
V = View
```

## Model

Representa os dados e sua estrutura.

Exemplo:

```python
class PostFilme(models.Model):
    titulo = models.CharField(max_length=250)
    nota = models.IntegerField()
```

O Model está diretamente relacionado ao banco de dados.

---

## Template

Define como os dados serão apresentados.

Normalmente é HTML com a linguagem de templates do Django.

Exemplo:

```django
<h1>{{ post.titulo }}</h1>

<p>Nota: {{ post.nota }}</p>
```

---

## View

Recebe uma requisição, executa a lógica necessária e retorna uma resposta.

Exemplo:

```python
def post_list(request):
    posts = PostFilme.publicados.all()

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Podemos pensar:

```text
Model
= dados

View
= lógica da requisição

Template
= apresentação
```

---

# 3. Projeto e App

No Django existe diferença entre **Project** e **App**.

## Project

É o sistema completo.

No nosso caso:

```text
CinePost
```

---

## App

É um módulo com determinada responsabilidade.

Exemplo:

```text
filmes
```

Um app pode possuir:

- vários Models;
- várias Views;
- várias URLs;
- vários Templates.

Portanto:

> Um App NÃO representa apenas uma tabela.

---

# 4. Estrutura básica

Nosso projeto possui uma estrutura parecida com:

```text
cinepost/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── filmes/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── migrations/
```

---

# 5. `manage.py`

O arquivo:

```text
manage.py
```

permite executar comandos relacionados ao projeto Django.

Exemplo:

```bash
python manage.py runserver
```

---

# 6. `settings.py`

É o arquivo principal de configurações.

Podemos pensar nele como o:

> Painel de controle do projeto.

Algumas configurações importantes:

```python
INSTALLED_APPS
MIDDLEWARE
DATABASES
LANGUAGE_CODE
TIME_ZONE
DEBUG
ALLOWED_HOSTS
```

---

# 7. `INSTALLED_APPS`

Lista os Apps ativados no projeto.

Exemplo:

```python
INSTALLED_APPS = [
    ...
    "filmes.apps.FilmesConfig",
]
```

Se criarmos um App mas não o registrarmos, o projeto pode não reconhecer corretamente alguns recursos dele.

---

# 8. Banco de dados

Durante os estudos estamos utilizando:

```text
SQLite
```

O arquivo normalmente é:

```text
db.sqlite3
```

Django também suporta bancos como:

- PostgreSQL;
- MySQL;
- Oracle.

---

# 9. Models

Models representam os dados da aplicação.

Nosso `PostFilme` possui uma estrutura parecida com:

```python
class PostFilme(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RA", "Rascunho"
        PUBLICADO = "PU", "Publicado"

    titulo = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250)

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts_filmes",
    )

    comentario = models.TextField()

    nota = models.IntegerField()

    publicado_em = models.DateTimeField(
        default=timezone.now
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.RASCUNHO,
    )

    def __str__(self):
        return self.titulo
```

---

# 10. Tipos de campos

## `CharField`

Texto curto.

```python
titulo = models.CharField(max_length=250)
```

---

## `TextField`

Texto grande.

```python
comentario = models.TextField()
```

---

## `IntegerField`

Número inteiro.

```python
nota = models.IntegerField()
```

---

## `SlugField`

Texto apropriado para URLs.

```python
slug = models.SlugField(max_length=250)
```

Exemplo:

```text
Interestelar

↓

interestelar
```

---

## `DateTimeField`

Data e horário.

```python
publicado_em = models.DateTimeField(
    default=timezone.now
)
```

---

# 11. Datas automáticas

## `default=timezone.now`

Define uma data inicial, mas permite alteração.

```python
publicado_em = models.DateTimeField(
    default=timezone.now
)
```

---

## `auto_now_add=True`

Preenche quando o objeto é criado.

```python
criado_em = models.DateTimeField(
    auto_now_add=True
)
```

---

## `auto_now=True`

Atualiza sempre que o objeto é salvo.

```python
atualizado_em = models.DateTimeField(
    auto_now=True
)
```

---

# 12. `TextChoices`

Usamos `TextChoices` para limitar possíveis valores.

```python
class Status(models.TextChoices):
    RASCUNHO = "RA", "Rascunho"
    PUBLICADO = "PU", "Publicado"
```

Cada opção possui:

```text
PUBLICADO
↓
nome usado no Python

"PU"
↓
valor salvo no banco

"Publicado"
↓
texto mostrado para humanos
```

Então:

```python
PostFilme.Status.PUBLICADO
```

representa o status publicado.

---

# 13. ForeignKey

Temos:

```python
autor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="posts_filmes",
)
```

Isso cria uma relação:

```text
Usuário 1
   ↓
pode possuir
   ↓
vários PostFilme
```

Cada `PostFilme` possui apenas um autor.

É uma relação:

```text
One-to-Many
```

ou:

```text
Many-to-One
```

---

# 14. `related_name`

Definimos:

```python
related_name="posts_filmes"
```

Isso permite fazer:

```python
user.posts_filmes.all()
```

Significa:

> Pegue todos os posts relacionados a esse usuário.

---

# 15. `on_delete=models.CASCADE`

Significa que, ao apagar o objeto principal, os dependentes também podem ser apagados.

Exemplo:

```text
Usuário
   ↓
PostFilme
```

Se apagarmos o usuário:

```python
user.delete()
```

os posts ligados a ele também serão removidos porque usamos:

```python
models.CASCADE
```

---

# 16. Meta

Podemos configurar comportamento padrão do Model usando:

```python
class Meta:
```

Exemplo:

```python
class Meta:
    ordering = ["-publicado_em"]

    indexes = [
        models.Index(
            fields=["-publicado_em"]
        ),
    ]
```

---

## `ordering`

```python
ordering = ["-publicado_em"]
```

Define a ordenação padrão.

O `-` significa:

```text
decrescente
```

Ou seja:

> Mais recentes primeiro.

---

## Índices

```python
models.Index(
    fields=["-publicado_em"]
)
```

Um índice pode melhorar o desempenho de consultas frequentes.

Porém índices também:

- ocupam espaço;
- possuem custo durante inserções e atualizações.

---

# 17. Migrations

Migration é o sistema usado para transformar mudanças dos Models em alterações no banco.

Fluxo:

```text
models.py
   ↓
makemigrations
   ↓
arquivo de migration
   ↓
migrate
   ↓
banco de dados
```

---

## Criar migration

```bash
python manage.py makemigrations
```

Ou:

```bash
python manage.py makemigrations filmes
```

Isso cria o plano da alteração.

---

## Aplicar migration

```bash
python manage.py migrate
```

Isso executa as mudanças no banco.

---

## Ver SQL da migration

```bash
python manage.py sqlmigrate filmes 0001
```

Isso NÃO altera o banco.

Apenas mostra o SQL que Django pretende executar.

---

# 18. ORM

ORM significa:

```text
Object-Relational Mapper
```

A ORM permite conversar com o banco utilizando Python.

Em vez de escrever:

```sql
SELECT *
FROM filmes_postfilme
WHERE nota >= 8;
```

podemos escrever:

```python
PostFilme.objects.filter(
    nota__gte=8
)
```

Fluxo:

```text
Python
   ↓
Django ORM
   ↓
SQL
   ↓
Banco
   ↓
resultado
   ↓
Django ORM
   ↓
Objeto Python
```

Portanto:

> A ORM é uma camada entre o Python e o banco de dados.

Ela não apenas gera SQL.

Ela também transforma registros do banco em objetos Python.

---

# 19. Manager

Todo Model possui um Manager.

O padrão é:

```python
objects
```

Exemplo:

```python
PostFilme.objects.all()
```

Podemos pensar:

```text
Model
   ↓
Manager
   ↓
QuerySet
   ↓
Banco
```

---

# 20. QuerySet

QuerySet representa uma consulta ao banco.

Exemplo:

```python
posts = PostFilme.objects.all()
```

`posts` é um QuerySet.

QuerySets são normalmente **lazy**.

Isso significa:

> Django tenta esperar até os dados realmente serem necessários antes de executar a consulta.

Podemos montar:

```python
posts = PostFilme.objects.all()

posts = posts.filter(
    status=PostFilme.Status.PUBLICADO
)

posts = posts.filter(
    nota__gte=8
)
```

Só quando os dados forem realmente necessários a consulta é executada.

---

# 21. Criando objetos

Podemos criar:

```python
post = PostFilme(
    titulo="Interestelar",
    nota=9,
    autor=user,
    comentario="Excelente filme",
)
```

Nesse momento ele está apenas na memória.

Para salvar:

```python
post.save()
```

Um objeto novo normalmente gera um:

```sql
INSERT
```

---

# 22. Atualizando objetos

Podemos alterar:

```python
post.titulo = "Novo título"
```

Mas a alteração ainda está apenas na memória.

Para persistir:

```python
post.save()
```

Agora Django executa algo equivalente a:

```sql
UPDATE
```

Regra:

```text
alterou objeto
↓
save()
↓
grava no banco
```

---

# 23. `.all()`

Retorna todos os objetos.

```python
PostFilme.objects.all()
```

Retorna um QuerySet.

---

# 24. `.get()`

Busca exatamente **um objeto**.

```python
PostFilme.objects.get(id=1)
```

Se não encontrar:

```text
DoesNotExist
```

Se encontrar mais de um:

```text
MultipleObjectsReturned
```

Por isso normalmente usamos `get()` quando esperamos exatamente um registro.

---

# 25. `.filter()`

Retorna um QuerySet.

```python
PostFilme.objects.filter(
    nota__gte=8
)
```

Pode retornar:

```text
0 objetos
1 objeto
vários objetos
```

Resumo:

```text
get()
→ quero exatamente um

filter()
→ quero todos que correspondem
```

---

# 26. Field Lookups

Django utiliza:

```text
campo__lookup
```

para consultas especiais.

---

## Igual

```python
filter(id=1)
```

Equivale a:

```python
filter(id__exact=1)
```

---

## `iexact`

Igual ignorando maiúsculas/minúsculas.

```python
filter(
    titulo__iexact="matrix"
)
```

---

## `contains`

Contém determinado texto.

```python
filter(
    titulo__contains="Matrix"
)
```

---

## `icontains`

Contém ignorando maiúsculas/minúsculas.

```python
filter(
    titulo__icontains="matrix"
)
```

Muito útil para buscas.

---

## `in`

Está dentro de uma lista.

```python
filter(
    id__in=[1, 3, 5]
)
```

---

## Comparações

```text
gt  → >
gte → >=
lt  → <
lte → <=
```

Exemplo:

```python
filter(nota__gte=8)
```

Significa:

> nota maior ou igual a 8.

---

## `startswith`

```python
filter(
    titulo__startswith="Homem"
)
```

---

## `istartswith`

Ignora maiúsculas/minúsculas.

```python
filter(
    titulo__istartswith="homem"
)
```

---

## `endswith`

```python
filter(
    titulo__endswith="2"
)
```

---

## Datas

Ano:

```python
filter(
    publicado_em__year=2026
)
```

Mês:

```python
filter(
    publicado_em__month=9
)
```

Dia:

```python
filter(
    publicado_em__day=3
)
```

---

# 27. Consultando relacionamentos

Os `__` também servem para atravessar relacionamentos.

Exemplo:

```python
PostFilme.objects.filter(
    autor__username="luciano"
)
```

Leia:

```text
autor
↓
username do autor
↓
igual a "luciano"
```

Também podemos fazer:

```python
PostFilme.objects.filter(
    autor__username__icontains="luc"
)
```

---

# 28. Vários filtros

```python
PostFilme.objects.filter(
    nota__gte=8,
    status=PostFilme.Status.PUBLICADO,
)
```

As condições são combinadas normalmente com:

```text
AND
```

Ou:

```text
nota >= 8
E
status = publicado
```

---

# 29. Encadeando filtros

Podemos fazer:

```python
posts = PostFilme.objects.filter(
    nota__gte=8
).filter(
    status=PostFilme.Status.PUBLICADO
)
```

Cada `filter()` devolve outro QuerySet.

---

# 30. `.exclude()`

Remove resultados que atendem a determinada condição.

```python
PostFilme.objects.exclude(
    titulo__startswith="Batman"
)
```

Resumo:

```text
filter()
→ quero

exclude()
→ não quero
```

---

# 31. `order_by()`

Ordem crescente:

```python
PostFilme.objects.order_by(
    "titulo"
)
```

Decrescente:

```python
PostFilme.objects.order_by(
    "-titulo"
)
```

Vários campos:

```python
PostFilme.objects.order_by(
    "autor",
    "titulo",
)
```

Aleatório:

```python
PostFilme.objects.order_by("?")
```

---

# 32. Limitando QuerySets

Primeiros cinco:

```python
PostFilme.objects.all()[:5]
```

Equivale aproximadamente a:

```sql
LIMIT 5
```

---

Do quarto até o sexto:

```python
PostFilme.objects.all()[3:6]
```

Como índices começam em zero:

```text
0 1 2 3 4 5
      ↑ ↑ ↑
```

Retorna três objetos.

---

Um único objeto:

```python
PostFilme.objects.all()[0]
```

---

Índices negativos não são suportados da mesma forma que listas Python:

```python
PostFilme.objects.all()[-1]
```

não deve ser usado.

---

# 33. `.count()`

Conta objetos.

```python
PostFilme.objects.count()
```

Ou:

```python
PostFilme.objects.filter(
    nota__gte=8
).count()
```

Pergunta:

> Quantos existem?

---

# 34. `.exists()`

Verifica se existe pelo menos um resultado.

```python
PostFilme.objects.filter(
    nota__gte=9
).exists()
```

Retorna:

```python
True
```

ou:

```python
False
```

Pergunta:

> Existe algum?

---

# 35. `.delete()`

Busca:

```python
post = PostFilme.objects.get(id=1)
```

Apaga:

```python
post.delete()
```

Isso remove o registro do banco.

---

# 36. Q Objects

Quando colocamos várias condições em um `filter()` normal, Django usa:

```text
AND
```

Exemplo:

```python
PostFilme.objects.filter(
    nota__gte=8,
    status=PostFilme.Status.PUBLICADO,
)
```

Significa:

```text
nota >= 8
E
publicado
```

Para fazer consultas com **OR**, usamos `Q`.

Importação:

```python
from django.db.models import Q
```

---

## OR

```python
PostFilme.objects.filter(
    Q(titulo__icontains="batman")
    |
    Q(titulo__icontains="superman")
)
```

Significa:

```text
Batman
OU
Superman
```

---

## AND com Q

Também podemos usar:

```python
Q(nota__gte=8) & Q(status=PostFilme.Status.PUBLICADO)
```

---

## NOT

```python
~Q(titulo__icontains="Batman")
```

Significa:

> título não contém Batman.

---

## Operadores Q

```text
& → AND
| → OR
^ → XOR
~ → NOT
```

Regra prática:

```text
AND simples
→ filter() normal

OR ou lógica complexa
→ Q()
```

---

# 37. Manager personalizado

Criamos:

```python
class PublicadosManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=self.model.Status.PUBLICADO
        )
```

E dentro do Model:

```python
objects = models.Manager()
publicados = PublicadosManager()
```

Agora:

```python
PostFilme.objects.all()
```

retorna:

> todos os posts.

Enquanto:

```python
PostFilme.publicados.all()
```

retorna:

> somente publicados.

---

Também podemos continuar filtrando:

```python
PostFilme.publicados.filter(
    nota__gte=8
)
```

Significa:

```text
PUBLICADO
E
nota >= 8
```

---

# 38. Admin

Django possui painel administrativo pronto.

URL padrão:

```text
/admin/
```

Para criar administrador:

```bash
python manage.py createsuperuser
```

Podemos registrar nosso Model:

```python
from django.contrib import admin

from .models import PostFilme


admin.site.register(PostFilme)
```

Ou personalizar:

```python
@admin.register(PostFilme)
class PostFilmeAdmin(admin.ModelAdmin):
    ...
```

O `ModelAdmin` modifica o painel administrativo.

Não modifica a estrutura do banco.

---

# 39. Views

Uma View:

> recebe um request, executa a lógica e retorna um response.

Exemplo:

```python
def post_list(request):
    posts = PostFilme.publicados.all()

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Podemos pensar:

```text
Shell
→ laboratório onde testamos consultas manualmente

View
→ código executado automaticamente quando chega uma requisição
```

---

# 40. List View

Serve para mostrar vários objetos.

```python
def post_list(request):
    posts = PostFilme.publicados.all()

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Aqui:

```python
{"posts": posts}
```

manda a variável `posts` para o template.

---

# 41. Detail View

Serve para mostrar um objeto específico.

```python
def post_detail(request, id):
    post = get_object_or_404(
        PostFilme.publicados,
        id=id,
    )

    return render(
        request,
        "filmes/post/detail.html",
        {"post": post},
    )
```

Aqui recebemos:

```python
id
```

pela URL.

---

# 42. `get_object_or_404()`

Importação:

```python
from django.shortcuts import get_object_or_404
```

Uso:

```python
post = get_object_or_404(
    PostFilme.publicados,
    id=id,
)
```

Significa:

> Procure esse objeto entre os publicados.

Se encontrar:

```text
retorna o objeto
```

Se não encontrar:

```text
404 Not Found
```

Isso substitui muito código de:

```python
try:
    ...
except DoesNotExist:
    raise Http404
```

---

# 43. URLs

Criamos:

```text
filmes/urls.py
```

Exemplo:

```python
from django.urls import path

from . import views


app_name = "filmes"


urlpatterns = [
    path(
        "",
        views.post_list,
        name="post_list",
    ),

    path(
        "<int:id>/",
        views.post_detail,
        name="post_detail",
    ),
]
```

---

# 44. Entendendo `path()`

Exemplo:

```python
path(
    "",
    views.post_list,
    name="post_list",
)
```

Temos três partes principais:

```text
1. caminho
2. View
3. nome da rota
```

---

## Primeiro argumento

```python
""
```

É o pedaço da URL.

Se o projeto já incluiu:

```text
/filmes/
```

o `""` significa:

> Não acrescente mais nada.

Resultado:

```text
/filmes/
```

---

## Segundo argumento

```python
views.post_list
```

Define:

> Qual View/lógica será executada.

---

## Terceiro argumento

```python
name="post_list"
```

É um apelido interno da rota.

Não aparece na URL.

Permite referenciar essa rota sem escrever o endereço manualmente.

---

# 45. Parâmetros de URL

Temos:

```python
path(
    "<int:id>/",
    views.post_detail,
    name="post_detail",
)
```

Se o usuário acessar:

```text
/filmes/5/
```

Django interpreta:

```python
id = 5
```

e executa:

```python
post_detail(
    request,
    id=5
)
```

---

# 46. Path converters

Alguns converters:

```text
<int:id>
<str:nome>
<slug:slug>
<uuid:id>
<path:caminho>
```

Exemplo:

```python
"<slug:slug>/"
```

poderia gerar:

```text
/filmes/interestelar/
```

---

# 47. `include()`

No:

```text
config/urls.py
```

podemos ter:

```python
from django.urls import include, path


urlpatterns = [
    path(
        "filmes/",
        include("filmes.urls"),
    ),
]
```

Isso significa:

> URLs que começam com `filmes/` devem continuar sendo analisadas pelo `filmes/urls.py`.

Então:

```text
config/urls.py

"filmes/"
+
filmes/urls.py

"<int:id>/"

=

/filmes/5/
```

---

# 48. Namespace

Definimos:

```python
app_name = "filmes"
```

Então podemos referenciar:

```text
filmes:post_list
```

ou:

```text
filmes:post_detail
```

Formato:

```text
namespace:nome_da_url
```

---

# 49. Templates

Templates definem como os dados aparecem.

Estrutura:

```text
filmes/
└── templates/
    └── filmes/
        ├── base.html
        └── post/
            ├── list.html
            └── detail.html
```

---

# 50. Linguagem de templates

Temos três conceitos principais.

---

## Variáveis

```django
{{ post.titulo }}
```

Mostra um valor.

---

## Template Tags

```django
{% for post in posts %}
{% endfor %}
```

Controlam a renderização.

---

## Filtros

```django
{{ post.comentario|truncatewords:30 }}
```

Transformam valores para exibição.

---

# 51. Template base

```django
{% load static %}

<!DOCTYPE html>

<html>

<head>

    <title>
        {% block title %}
        {% endblock %}
    </title>

</head>

<body>

    {% block content %}
    {% endblock %}

</body>

</html>
```

---

# 52. Herança de Templates

Uma página pode herdar do `base.html`:

```django
{% extends "filmes/base.html" %}
```

E preencher:

```django
{% block title %}
CinePost
{% endblock %}
```

e:

```django
{% block content %}
...
{% endblock %}
```

Isso evita repetir HTML.

---

# 53. Arquivos estáticos

Usamos:

```django
{% load static %}
```

Depois:

```django
{% static 'filmes/css/filmes.css' %}
```

Arquivos estáticos incluem:

```text
CSS
JavaScript
imagens
ícones
```

Uma estrutura recomendada:

```text
filmes/
└── static/
    └── filmes/
        └── css/
            └── filmes.css
```

---

# 54. List Template

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}
CinePost
{% endblock %}

{% block content %}

    <h1>CinePost</h1>

    {% for post in posts %}

        <h2>
            <a href="{% url 'filmes:post_detail' post.id %}">
                {{ post.titulo }}
            </a>
        </h2>

        <p>
            Publicado por {{ post.autor }}
        </p>

        {{ post.comentario|truncatewords:30|linebreaks }}

    {% endfor %}

{% endblock %}
```

---

# 55. `{% url %}`

Nunca é bom espalhar URLs manualmente pelos templates.

Em vez de:

```html
<a href="/filmes/5/">
```

usamos:

```django
{% url 'filmes:post_detail' post.id %}
```

O Django encontra a URL pelo:

```text
namespace
+
name
+
parâmetros
```

Exemplo:

```text
filmes
:
post_detail
+
id = 5
```

Resultado:

```text
/filmes/5/
```

Isso é parecido com o `url_for()` do Flask.

---

# 56. Template Filters

## `truncatewords`

```django
{{ post.comentario|truncatewords:30 }}
```

Limita o texto a aproximadamente 30 palavras.

---

## `linebreaks`

```django
{{ post.comentario|linebreaks }}
```

Converte quebras de linha do texto para HTML apropriado.

---

## Encadeamento

```django
{{ post.comentario|truncatewords:30|linebreaks }}
```

Fluxo:

```text
comentário
↓
truncatewords
↓
linebreaks
↓
resultado
```

---

# 57. Detail Template

```django
{% extends "filmes/base.html" %}

{% block title %}
    {{ post.titulo }}
{% endblock %}

{% block content %}

    <h1>
        {{ post.titulo }}
    </h1>

    <p>
        Publicado por {{ post.autor }}
    </p>

    <p>
        Nota: {{ post.nota }}
    </p>

    {{ post.comentario|linebreaks }}

{% endblock %}
```

Aqui temos apenas:

```python
post
```

porque a Detail View envia apenas um objeto.

---

# 58. Request / Response Cycle

Esse é um dos conceitos mais importantes do capítulo.

Imagine:

```text
/filmes/33/
```

O fluxo é:

```text
Navegador
   ↓
HTTP Request
   ↓
URL
   ↓
urls.py
   ↓
View
   ↓
ORM
   ↓
Banco
   ↓
Objeto PostFilme
   ↓
Template
   ↓
HTML
   ↓
HttpResponse
   ↓
Navegador
```

---

## Passo 1

Usuário acessa:

```text
/filmes/33/
```

---

## Passo 2

Django procura a primeira URL correspondente.

```python
path(
    "<int:id>/",
    views.post_detail,
    name="post_detail",
)
```

Então:

```python
id = 33
```

---

## Passo 3

Django executa:

```python
post_detail(
    request,
    id=33
)
```

---

## Passo 4

A View usa ORM:

```python
post = get_object_or_404(
    PostFilme.publicados,
    id=id,
)
```

---

## Passo 5

ORM gera SQL e consulta o banco.

---

## Passo 6

O resultado vira um objeto Python:

```python
post
```

---

## Passo 7

A View manda o objeto para o Template:

```python
{"post": post}
```

---

## Passo 8

O Template gera HTML.

---

## Passo 9

`render()` retorna:

```text
HttpResponse
```

---

## Passo 10

O navegador recebe e mostra a página.

---

# 59. View, URL e Template

Resumo:

```text
URL
→ decide qual View chamar

View
→ executa a lógica

Model / ORM
→ trabalha com os dados

Template
→ apresenta os dados

HttpResponse
→ resposta enviada ao usuário
```

---

# 60. Comparação com Flask

No Flask:

```python
@app.route("/filmes")
def filmes():
    # lógica
```

A rota e a função ficam muito próximas.

No Django:

```python
# urls.py

path(
    "filmes/",
    views.filmes
)
```

E:

```python
# views.py

def filmes(request):
    # lógica
```

Django separa explicitamente:

```text
rota
↓
View
```

---

# 61. Comandos importantes

## Criar projeto

```bash
django-admin startproject config .
```

---

## Criar App

```bash
python manage.py startapp filmes
```

---

## Criar migrations

```bash
python manage.py makemigrations
```

---

## Aplicar migrations

```bash
python manage.py migrate
```

---

## Ver SQL

```bash
python manage.py sqlmigrate filmes 0001
```

---

## Rodar servidor

```bash
python manage.py runserver
```

Servidor padrão:

```text
http://127.0.0.1:8000/
```

---

## Outra porta

```bash
python manage.py runserver 8001
```

---

## Shell do Django

```bash
python manage.py shell
```

O shell é nosso laboratório para testar:

- ORM;
- Models;
- QuerySets;
- consultas.

---

## Criar superusuário

```bash
python manage.py createsuperuser
```

---

# 62. Fluxo de trabalho básico

Uma sequência comum durante desenvolvimento Django:

```text
Criar projeto
↓
Criar App
↓
Registrar App
↓
Criar Models
↓
makemigrations
↓
migrate
↓
Registrar no Admin
↓
Criar Views
↓
Criar URLs
↓
Criar Templates
↓
runserver
↓
Testar
```

---

# 63. Resumo da ORM

```text
CREATE
→ objects.create()
→ objeto + save()

READ
→ all()
→ get()
→ filter()

UPDATE
→ alterar atributo
→ save()

DELETE
→ delete()
```

CRUD:

```text
C = Create
R = Read
U = Update
D = Delete
```

---

# 64. Resumo dos QuerySets

| Método | Função |
|---|---|
| `.all()` | Todos |
| `.get()` | Exatamente um |
| `.filter()` | Filtrar |
| `.exclude()` | Excluir resultados |
| `.order_by()` | Ordenar |
| `.count()` | Contar |
| `.exists()` | Verificar existência |
| `.delete()` | Apagar |
| `[:5]` | Limitar |
| `Q()` | Consultas complexas |

---

# 65. Resumo dos Lookups

| Lookup | Significado |
|---|---|
| `exact` | Igual |
| `iexact` | Igual ignorando maiúsculas |
| `contains` | Contém |
| `icontains` | Contém ignorando maiúsculas |
| `in` | Está em uma coleção |
| `gt` | Maior que |
| `gte` | Maior ou igual |
| `lt` | Menor que |
| `lte` | Menor ou igual |
| `startswith` | Começa com |
| `istartswith` | Começa com ignorando maiúsculas |
| `endswith` | Termina com |
| `iendswith` | Termina com ignorando maiúsculas |
| `year` | Ano |
| `month` | Mês |
| `day` | Dia |

---

# 66. Resumo dos Templates

```django
{{ variavel }}
```

Mostra dados.

```django
{% tag %}
```

Executa instruções do Template.

```django
{{ variavel|filtro }}
```

Formata dados.

```django
{% extends %}
```

Herda outro Template.

```django
{% block %}
```

Define área substituível.

```django
{% url %}
```

Gera URLs pelo nome.

```django
{% static %}
```

Gera caminho de arquivos estáticos.

---

# 67. O conceito principal do capítulo

O capítulo inteiro pode ser resumido neste fluxo:

```text
USUÁRIO
   ↓
URL
   ↓
VIEW
   ↓
ORM
   ↓
MODEL
   ↓
BANCO DE DADOS
   ↓
VIEW
   ↓
TEMPLATE
   ↓
HTTP RESPONSE
   ↓
USUÁRIO
```

Ou em uma frase:

> **A URL encontra a View, a View executa a lógica, a ORM conversa com o banco, o Template monta a apresentação e Django devolve uma resposta HTTP.**

---

# 68. Mapa mental final

```text
Django
│
├── Project
│   └── sistema completo
│
├── Apps
│   └── módulos do sistema
│
├── Models
│   └── estrutura dos dados
│
├── ORM
│   └── comunicação Python ↔ banco
│
├── Managers
│   └── entrada para consultas
│
├── QuerySets
│   └── consultas
│
├── URLs
│   └── encontram Views
│
├── Views
│   └── lógica da requisição
│
├── Templates
│   └── apresentação
│
├── Static
│   └── CSS / JS / imagens
│
├── Admin
│   └── administração dos Models
│
└── Migrations
    └── alterações da estrutura do banco
```

---

# Conclusão

Neste capítulo aprendemos a montar o primeiro fluxo completo de uma aplicação Django.

Criamos:

```text
Model
↓
Migration
↓
Banco
↓
Admin
↓
ORM
↓
Manager
↓
View
↓
URL
↓
Template
↓
Página
```

A partir daqui já temos a base necessária para construir funcionalidades maiores no **CinePost**.

O conceito mais importante para levar para os próximos capítulos é:

```text
Request
↓
URL
↓
View
↓
Dados
↓
Template
↓
Response
```

Essa é a base sobre a qual praticamente todo o restante do Django será construído.