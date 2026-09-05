# Django — Paginação e Class-Based Views com `ListView`

## 1. O que estávamos fazendo antes

Inicialmente, a página que lista os posts do CinePost foi criada usando uma **Function-Based View (FBV)**.

Exemplo:

```python
def post_list(request):
    post_list = PostFilme.publicados.all()

    paginator = Paginator(post_list, 3)

    page_number = request.GET.get("page", 1)

    posts = paginator.get_page(page_number)

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Essa função fazia várias tarefas:

```text
Receber a requisição
        ↓
Buscar posts publicados
        ↓
Criar o Paginator
        ↓
Descobrir qual página foi pedida
        ↓
Pegar os posts daquela página
        ↓
Enviar os posts para o template
        ↓
Retornar a resposta
```

Ela funciona perfeitamente.

Porém, listar objetos com paginação é uma tarefa extremamente comum em aplicações web.

Por isso, o Django já possui uma classe pronta chamada:

```python
ListView
```

---

# 2. O que é uma Class-Based View?

Até agora usamos views como funções:

```python
def post_list(request):
    ...
```

Isso é chamado de:

```text
Function-Based View
FBV
```

Também podemos criar views usando classes:

```python
class PostListView(ListView):
    ...
```

Isso é chamado de:

```text
Class-Based View
CBV
```

As duas continuam tendo a mesma responsabilidade:

```text
Request
   ↓
View
   ↓
Lógica
   ↓
Response
```

A diferença está em **como escrevemos e organizamos a View**.

---

# 3. Para que servem as Class-Based Views?

A principal vantagem é aproveitar comportamentos que o Django já implementou.

Por exemplo, praticamente todo sistema precisa:

```text
listar objetos
mostrar detalhes
criar objetos
editar objetos
excluir objetos
```

O Django fornece classes prontas para essas situações:

```text
ListView
    → listar objetos

DetailView
    → mostrar um objeto

CreateView
    → criar um objeto

UpdateView
    → editar um objeto

DeleteView
    → excluir um objeto
```

Em vez de escrever toda a lógica novamente, configuramos uma dessas classes.

---

# 4. A `ListView`

Para listar os posts do CinePost podemos usar:

```python
from django.views.generic import ListView
```

Depois criamos:

```python
class PostListView(ListView):
    queryset = PostFilme.publicados.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "filmes/post/list.html"
```

Essa classe substitui nossa antiga função:

```python
def post_list(request):
    ...
```

---

# 5. Entendendo cada parte da `PostListView`

## `class PostListView(ListView)`

```python
class PostListView(ListView):
```

Estamos criando nossa própria View e herdando o comportamento da:

```python
ListView
```

A `ListView` já sabe fazer coisas como:

```text
buscar objetos
criar contexto
paginar
processar GET
renderizar template
retornar resposta
```

Nós apenas configuramos o que queremos.

---

# 6. `queryset`

```python
queryset = PostFilme.publicados.all()
```

Define quais objetos serão listados.

No CinePost queremos somente posts publicados.

Por isso usamos nosso Manager:

```python
PostFilme.publicados.all()
```

Se usássemos:

```python
model = PostFilme
```

o Django criaria automaticamente algo equivalente a:

```python
PostFilme.objects.all()
```

Mas isso poderia incluir:

```text
publicados
+
rascunhos
```

Como queremos apenas publicados, usamos um QuerySet personalizado:

```python
queryset = PostFilme.publicados.all()
```

---

# 7. `context_object_name`

```python
context_object_name = "posts"
```

Define o nome da variável que estará disponível no template.

Assim podemos escrever:

```django
{% for post in posts %}
    {{ post.titulo }}
{% endfor %}
```

Se não definíssemos:

```python
context_object_name = "posts"
```

a `ListView` utilizaria por padrão:

```text
object_list
```

Então precisaríamos fazer:

```django
{% for post in object_list %}
```

`posts` é mais claro para nosso projeto.

---

# 8. `paginate_by`

```python
paginate_by = 3
```

Significa:

> Mostrar no máximo 3 posts por página.

Com isso, o Django faz automaticamente a paginação.

Antes nós precisávamos escrever:

```python
paginator = Paginator(post_list, 3)

page_number = request.GET.get("page", 1)

posts = paginator.get_page(page_number)
```

Com a `ListView`:

```python
paginate_by = 3
```

substitui praticamente toda essa lógica.

---

# 9. `template_name`

```python
template_name = "filmes/post/list.html"
```

Define qual template será usado para mostrar os resultados.

No nosso projeto:

```text
filmes/
└── templates/
    └── filmes/
        └── post/
            └── list.html
```

Por isso:

```python
template_name = "filmes/post/list.html"
```

---

# 10. View completa

No `views.py`:

```python
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import PostFilme


class PostListView(ListView):
    queryset = PostFilme.publicados.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "filmes/post/list.html"
```

Nossa outra View pode continuar normalmente como função:

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

Não existe problema em misturar:

```text
Class-Based View
+
Function-Based View
```

no mesmo projeto.

---

# 11. Alterando a URL

Antes nossa URL chamava uma função:

```python
path(
    "",
    views.post_list,
    name="post_list",
)
```

Como agora temos uma classe, usamos:

```python
path(
    "",
    views.PostListView.as_view(),
    name="post_list",
)
```

O `urls.py` fica:

```python
from django.urls import path

from . import views


app_name = "filmes"


urlpatterns = [
    path(
        "",
        views.PostListView.as_view(),
        name="post_list",
    ),

    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
]
```

---

# 12. O que é `.as_view()`?

Uma URL do Django precisa apontar para algo que funcione como uma View.

Uma Function-Based View já é uma função:

```python
views.post_list
```

Mas:

```python
PostListView
```

é uma classe.

Por isso usamos:

```python
PostListView.as_view()
```

O `.as_view()` transforma a classe em algo que o sistema de URLs do Django consegue chamar como View.

Mentalmente:

```text
PostListView
    ↓
.as_view()
    ↓
View utilizável pelo sistema de URLs
```

Por isso:

```python
views.PostListView.as_view()
```

---

# 13. Paginação automática da `ListView`

Com:

```python
paginate_by = 3
```

a `ListView` cria automaticamente informações de paginação.

Quando acessamos:

```text
/filmes/
```

temos a primeira página.

Quando acessamos:

```text
/filmes/?page=2
```

temos a segunda.

Quando acessamos:

```text
/filmes/?page=3
```

temos a terceira.

O:

```text
?page=2
```

continua sendo um parâmetro GET.

Não é uma rota nova.

A rota continua:

```text
/filmes/
```

---

# 14. `posts` e `page_obj`

Com nossa antiga Function-Based View, fazíamos:

```python
posts = paginator.get_page(page_number)
```

Nesse caso `posts` era o próprio objeto de página.

Com a `ListView`, o Django fornece duas variáveis importantes.

## `posts`

Como definimos:

```python
context_object_name = "posts"
```

podemos fazer:

```django
{% for post in posts %}
```

Ela é usada para percorrer os objetos daquela página.

---

## `page_obj`

A `ListView` também cria:

```text
page_obj
```

Esse é o objeto responsável pelas informações da paginação.

Ele possui coisas como:

```text
page_obj.number
page_obj.has_previous
page_obj.previous_page_number
page_obj.has_next
page_obj.next_page_number
page_obj.paginator.num_pages
```

Por isso nosso template genérico de paginação deve receber:

```django
page_obj
```

---

# 15. Template `list.html`

Nosso template pode ficar assim:

```django
{% extends "filmes/base.html" %}

{% block title %}
    CinePost
{% endblock %}

{% block content %}

    <h1>CinePost</h1>

    {% for post in posts %}

        <h2>
            <a href="{{ post.get_absolute_url }}">
                {{ post.titulo }}
            </a>
        </h2>

        <p class="date">
            Publicado em {{ post.publicado_em }}
            por {{ post.autor }}
        </p>

        {{ post.comentario|truncatewords:30|linebreaks }}

    {% endfor %}

    {% include "pagination.html" with page=page_obj %}

{% endblock %}
```

---

# 16. Template reutilizável de paginação

Criamos:

```text
templates/pagination.html
```

Com:

```django
<div class="pagination">
    <span class="step-links">

        {% if page.has_previous %}
            <a href="?page={{ page.previous_page_number }}">
                Anterior
            </a>
        {% endif %}

        <span class="current">
            Página {{ page.number }}
            de {{ page.paginator.num_pages }}
        </span>

        {% if page.has_next %}
            <a href="?page={{ page.next_page_number }}">
                Próxima
            </a>
        {% endif %}

    </span>
</div>
```

Depois incluímos:

```django
{% include "pagination.html" with page=page_obj %}
```

---

# 17. Por que o `pagination.html` é reutilizável?

Porque ele não sabe nada sobre:

```text
PostFilme
posts
comentários
usuários
produtos
```

Ele simplesmente espera receber um objeto chamado:

```text
page
```

Então podemos usar futuramente:

```django
{% include "pagination.html" with page=page_obj %}
```

em várias páginas do sistema.

Por exemplo:

```text
lista de filmes
lista de comentários
lista de usuários
lista de avaliações
```

O mesmo template pode servir para todas.

---

# 18. Antes e depois da `ListView`

## Antes — Function-Based View

```python
def post_list(request):
    post_list = PostFilme.publicados.all()

    paginator = Paginator(post_list, 3)

    page_number = request.GET.get("page", 1)

    posts = paginator.get_page(page_number)

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )
```

Nós precisávamos controlar:

```text
QuerySet
Paginator
GET
página atual
render
contexto
```

---

## Depois — Class-Based View

```python
class PostListView(ListView):
    queryset = PostFilme.publicados.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "filmes/post/list.html"
```

Nós apenas configuramos:

```text
O que listar?
→ queryset

Como chamar no template?
→ context_object_name

Quantos por página?
→ paginate_by

Qual template?
→ template_name
```

O Django cuida do resto.

---

# 19. Fluxo da `ListView`

Quando o usuário acessa:

```text
/filmes/?page=2
```

o fluxo é aproximadamente:

```text
Browser
   ↓
GET /filmes/?page=2
   ↓
urls.py
   ↓
PostListView.as_view()
   ↓
ListView
   ↓
queryset
PostFilme.publicados.all()
   ↓
paginação
3 posts por página
   ↓
página 2
   ↓
contexto
posts + page_obj
   ↓
filmes/post/list.html
   ↓
HTML
   ↓
Response
   ↓
Browser
```

---

# 20. Tratamento de páginas inválidas

Antes usamos:

```python
paginator.get_page(page_number)
```

O `get_page()` era tolerante com valores errados.

Por exemplo:

```text
?page=abc
```

poderia cair na primeira página.

E:

```text
?page=99999
```

poderia cair na última página.

A paginação padrão da `ListView` tem outro comportamento.

Quando uma página não pode ser encontrada, ela pode responder:

```text
404 Not Found
```

Isso é comportamento esperado.

A própria `ListView` faz o tratamento da paginação.

---

# 21. Class-Based View não cria uma funcionalidade nova

É importante lembrar:

A CBV não faz algo que seria impossível fazer com uma função.

Tudo que fazemos com:

```python
class PostListView(ListView):
```

também poderia ser feito usando:

```python
def post_list(request):
```

A vantagem da CBV é:

```text
menos código repetitivo
+
reutilização
+
comportamentos prontos do Django
+
organização
```

---

# 22. Quando usar Function-Based View?

FBV é ótima quando a lógica é:

```text
simples
específica
diferente do padrão
```

Exemplo:

```python
def alguma_view(request):
    ...
```

Às vezes uma função deixa o fluxo muito mais fácil de entender.

---

# 23. Quando usar Class-Based View?

CBV é especialmente interessante quando a funcionalidade é padrão:

```text
listar
detalhar
criar
editar
excluir
```

Porque o Django já possui estruturas prontas.

Exemplo:

```text
Lista de posts
→ ListView

Detalhes de um post
→ DetailView

Cadastro
→ CreateView

Edição
→ UpdateView

Exclusão
→ DeleteView
```

---

# 24. Mapa mental

```text
VIEW
│
├── Function-Based View
│
│   └── def post_list(request):
│
└── Class-Based View
    │
    ├── View
    │   └── classe básica
    │
    ├── ListView
    │   └── listar objetos
    │
    ├── DetailView
    │   └── mostrar um objeto
    │
    ├── CreateView
    │   └── criar
    │
    ├── UpdateView
    │   └── editar
    │
    └── DeleteView
        └── excluir
```

---

# 25. Mapa mental da nossa `PostListView`

```text
PostListView
│
├── queryset
│   └── PostFilme.publicados.all()
│
├── context_object_name
│   └── posts
│
├── paginate_by
│   └── 3
│
└── template_name
    └── filmes/post/list.html
```

Depois:

```text
urls.py
↓
views.PostListView.as_view()
↓
ListView executa
↓
posts
+
page_obj
↓
list.html
```

---

# 26. Resumo para decorar

## Function-Based View

Nós dizemos **como fazer**:

```text
busque os dados
crie o paginator
pegue page
pagine
crie contexto
renderize
```

## Class-Based View

Nós configuramos principalmente **o que queremos**:

```python
class PostListView(ListView):
    queryset = PostFilme.publicados.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "filmes/post/list.html"
```

E o Django executa o comportamento padrão.

---

# Ideia principal

> `ListView` é uma Class-Based View pronta do Django especializada em listar objetos.

> Ela pode substituir uma Function-Based View de listagem e eliminar boa parte do código repetitivo.

> `queryset` define o que será listado.

> `context_object_name` define o nome dos objetos no template.

> `paginate_by` ativa a paginação automática.

> `template_name` define qual HTML será renderizado.

> `page_obj` contém as informações da paginação.

> `.as_view()` permite que uma classe seja utilizada como View no `urls.py`.

## Em uma frase

**Class-Based View é uma forma de aproveitar estruturas prontas do Django e configurar o comportamento necessário, em vez de implementar manualmente toda a lógica repetitiva de uma View.**