# Django — Formulário para recomendar posts por e-mail

## Objetivo

Criamos uma funcionalidade para permitir que o usuário:

```text
abra um post
↓
clique em recomendar
↓
preencha um formulário
↓
envie por POST
↓
Django valide os dados
↓
mande um e-mail
↓
mostre uma mensagem de sucesso
```

---

# 1. Criando o formulário

Criamos:

```text
filmes/forms.py
```

Com:

```python
from django import forms


class RecomendarPostForm(forms.Form):
    nome = forms.CharField(max_length=25)
    email = forms.EmailField()
    destinatario = forms.EmailField()
    comentario = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
```

---

# 2. `Form` x `ModelForm`

## `forms.Form`

Usamos quando o formulário não precisa criar ou editar diretamente um Model.

Exemplo:

```text
recomendar por e-mail
formulário de contato
busca
```

## `forms.ModelForm`

Usamos quando o formulário está ligado a um Model.

Exemplo:

```text
criar PostFilme
editar PostFilme
editar usuário
```

---

# 3. Fields

## `CharField`

```python
nome = forms.CharField(max_length=25)
```

Campo de texto.

Valida:

```text
obrigatório
máximo de 25 caracteres
```

---

## `EmailField`

```python
email = forms.EmailField()
```

Valida se o valor possui formato de e-mail.

Também usamos:

```python
destinatario = forms.EmailField()
```

---

## Campo opcional

```python
required=False
```

Significa:

> esse campo pode ficar vazio.

Usamos no comentário:

```python
comentario = forms.CharField(
    required=False,
)
```

---

# 4. Widget

O Field define principalmente:

```text
tipo de dado
+
validação
```

O Widget define principalmente:

```text
como aparece no HTML
```

Exemplo:

```python
widget=forms.Textarea
```

faz o campo ser renderizado como:

```html
<textarea></textarea>
```

em vez de:

```html
<input type="text">
```

---

# 5. Criando a View

Criamos uma View que serve tanto para mostrar o formulário quanto para processá-lo.

```python
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

from .forms import RecomendarPostForm
from .models import PostFilme


def recomendar_post(request, post_id):
    post = get_object_or_404(
        PostFilme.publicados,
        id=post_id,
    )

    enviado = False

    if request.method == "POST":
        form = RecomendarPostForm(request.POST)

        if form.is_valid():
            dados = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            assunto = (
                f"{dados['nome']} ({dados['email']}) "
                f"recomenda o post {post.titulo}"
            )

            mensagem = (
                f"Veja {post.titulo} em:\n"
                f"{post_url}\n\n"
                f"Comentário de {dados['nome']}:\n"
                f"{dados['comentario']}"
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=None,
                recipient_list=[dados["destinatario"]],
            )

            enviado = True

    else:
        form = RecomendarPostForm()

    return render(
        request,
        "filmes/post/share.html",
        {
            "post": post,
            "form": form,
            "enviado": enviado,
        },
    )
```

---

# 6. GET e POST na mesma View

Essa View possui dois comportamentos.

## GET

Quando o usuário apenas abre a página:

```text
GET
↓
formulário vazio
```

Código:

```python
form = RecomendarPostForm()
```

---

## POST

Quando o usuário envia o formulário:

```text
POST
↓
request.POST
↓
validação
```

Código:

```python
form = RecomendarPostForm(request.POST)
```

---

# 7. `request.POST`

Contém os dados enviados pelo formulário.

Exemplo conceitual:

```text
nome=Luciano
email=luciano@gmail.com
destinatario=amigo@gmail.com
comentario=Veja esse filme
```

Esses são dados brutos.

Por isso primeiro passamos para:

```python
RecomendarPostForm(request.POST)
```

---

# 8. `is_valid()`

```python
if form.is_valid():
```

Valida os campos.

Exemplo:

```text
email válido?
destinatário válido?
nome dentro do tamanho?
campo obrigatório preenchido?
```

Se tudo estiver certo:

```python
True
```

Se houver erro:

```python
False
```

---

# 9. `cleaned_data`

Depois da validação:

```python
dados = form.cleaned_data
```

O `cleaned_data` contém os dados já:

```text
validados
normalizados
processados
```

Exemplo:

```python
dados["nome"]
dados["email"]
dados["destinatario"]
dados["comentario"]
```

É preferível usar:

```python
form.cleaned_data
```

em vez de continuar usando os dados crus de:

```python
request.POST
```

---

# 10. `form.errors`

Se o formulário for inválido:

```python
form.errors
```

contém os erros de validação.

O próprio template pode renderizar esses erros automaticamente.

---

# 11. URL completa do post

Já tínhamos:

```python
post.get_absolute_url()
```

que pode gerar:

```text
/filmes/2026/9/5/interestelar/
```

Isso é uma URL relativa.

Para e-mail precisamos de uma URL completa.

Usamos:

```python
request.build_absolute_uri(
    post.get_absolute_url()
)
```

Resultado em desenvolvimento:

```text
http://127.0.0.1:8000/filmes/2026/9/5/interestelar/
```

Em produção poderia ser:

```text
https://cinepost.com/filmes/2026/9/5/interestelar/
```

---

# 12. `get_absolute_url()` x `build_absolute_uri()`

## `get_absolute_url()`

Retorna o caminho do objeto:

```text
/filmes/2026/9/5/interestelar/
```

## `build_absolute_uri()`

Adiciona:

```text
protocolo
+
domínio
```

Resultado:

```text
http://127.0.0.1:8000/filmes/2026/9/5/interestelar/
```

---

# 13. Montando o assunto

```python
assunto = (
    f"{dados['nome']} ({dados['email']}) "
    f"recomenda o post {post.titulo}"
)
```

Exemplo:

```text
Luciano (luciano@gmail.com) recomenda o post Interestelar
```

---

# 14. Montando a mensagem

```python
mensagem = (
    f"Veja {post.titulo} em:\n"
    f"{post_url}\n\n"
    f"Comentário de {dados['nome']}:\n"
    f"{dados['comentario']}"
)
```

Exemplo:

```text
Veja Interestelar em:
http://127.0.0.1:8000/filmes/2026/9/5/interestelar/

Comentário de Luciano:
Assiste esse filme!
```

---

# 15. `send_mail()`

Importamos:

```python
from django.core.mail import send_mail
```

Depois:

```python
send_mail(
    subject=assunto,
    message=mensagem,
    from_email=None,
    recipient_list=[dados["destinatario"]],
)
```

---

# 16. Parâmetros do `send_mail()`

## `subject`

Assunto do e-mail.

```python
subject=assunto
```

## `message`

Corpo do e-mail.

```python
message=mensagem
```

## `from_email`

Remetente.

```python
from_email=None
```

Com `None`, o Django usa:

```python
DEFAULT_FROM_EMAIL
```

## `recipient_list`

Lista de destinatários.

```python
recipient_list=[
    dados["destinatario"]
]
```

Mesmo com apenas um destinatário, deve ser uma lista.

---

# 17. `enviado`

Criamos:

```python
enviado = False
```

Depois do envio:

```python
enviado = True
```

Isso serve para o template saber o que mostrar.

```text
False
→ mostrar formulário

True
→ mostrar mensagem de sucesso
```

---

# 18. Criando a rota

No `filmes/urls.py`:

```python
path(
    "<int:post_id>/recomendar/",
    views.recomendar_post,
    name="recomendar_post",
)
```

Exemplo:

```text
/filmes/7/recomendar/
```

passa:

```python
post_id = 7
```

para a View.

---

# 19. URL da ação x URL do post

São duas URLs diferentes.

## URL para recomendar

```text
/filmes/7/recomendar/
```

Serve para executar a ação.

## URL oficial do post

```text
/filmes/2026/9/5/interestelar/
```

É a URL canônica do objeto.

A View de recomendação usa o ID apenas para localizar o post.

---

# 20. Criando o template

Criamos:

```text
filmes/templates/filmes/post/share.html
```

Com:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Recomendar post
{% endblock %}

{% block content %}

    {% if enviado %}

        <h1>E-mail enviado com sucesso</h1>

        <p>
            "{{ post.titulo }}" foi enviado com sucesso para
            {{ form.cleaned_data.destinatario }}.
        </p>

    {% else %}

        <h1>
            Recomendar "{{ post.titulo }}" por e-mail
        </h1>

        <form method="post">

            {{ form.as_p }}

            {% csrf_token %}

            <input type="submit" value="Enviar e-mail">

        </form>

    {% endif %}

{% endblock %}
```

---

# 21. `{{ form.as_p }}`

O Django pode renderizar automaticamente os campos do Form.

```django
{{ form.as_p }}
```

Significa:

> renderize cada campo dentro de um `<p>`.

Exemplo conceitual:

```html
<p>
    <label>Nome:</label>
    <input type="text">
</p>
```

---

# 22. Outras formas de renderizar

Também existem:

```django
{{ form.as_ul }}
```

e:

```django
{{ form.as_table }}
```

Mas `as_p` é simples para começar.

---

# 23. CSRF

Em formulário POST usamos:

```django
{% csrf_token %}
```

O Django gera um campo escondido:

```html
<input
    type="hidden"
    name="csrfmiddlewaretoken"
    value="..."
>
```

Esse token ajuda a proteger contra ataques CSRF.

---

# 24. O que é CSRF?

CSRF significa:

```text
Cross-Site Request Forgery
```

É quando outro site tenta fazer seu navegador executar uma ação em um site onde você está autenticado.

Fluxo da proteção:

```text
Django gera token
↓
formulário recebe token
↓
usuário envia POST
↓
token volta para Django
↓
Django verifica
```

Se o token estiver ausente ou inválido:

```text
403 Forbidden
```

---

# 25. Regra importante

Em formulários internos enviados via POST:

```django
<form method="post">

    {% csrf_token %}

</form>
```

---

# 26. Adicionando link no `detail.html`

No detalhe do post:

```django
<p>
    <a href="{% url 'filmes:recomendar_post' post.id %}">
        Recomendar este post
    </a>
</p>
```

---

# 27. `{% url %}`

```django
{% url 'filmes:recomendar_post' post.id %}
```

usa:

```text
namespace
+
nome da rota
+
parâmetro
```

Exemplo:

```python
post.id = 7
```

gera:

```text
/filmes/7/recomendar/
```

---

# 28. Validação do navegador

Como o Django pode gerar:

```html
<input type="email">
```

o navegador também pode validar alguns campos antes do envio.

Exemplo:

```text
banana
```

em um campo de e-mail pode ser rejeitado pelo navegador.

Então o formulário nem chega ao Django.

---

# 29. Validação do navegador x Django

Existem duas camadas:

```text
Navegador
↓
validação HTML
```

e:

```text
Servidor Django
↓
Form.is_valid()
```

A validação do navegador melhora a experiência.

Mas a validação do servidor continua obrigatória.

Nunca devemos confiar apenas no navegador.

---

# 30. `novalidate`

Para testar especificamente a validação do Django:

```html
<form method="post" novalidate>
```

O:

```text
novalidate
```

desliga temporariamente a validação automática do navegador.

Assim podemos enviar valores errados e ver os erros gerados pelo Django.

Depois do teste, removemos:

```text
novalidate
```

---

# 31. Fluxo completo da funcionalidade

```text
Usuário abre um PostFilme
        ↓
detail.html
        ↓
"Recomendar este post"
        ↓
/filmes/7/recomendar/
        ↓
GET
        ↓
recomendar_post()
        ↓
RecomendarPostForm()
        ↓
share.html
        ↓
form.as_p
        ↓
usuário preenche
        ↓
POST
        ↓
csrf_token
        ↓
RecomendarPostForm(request.POST)
        ↓
is_valid()
        ↓
cleaned_data
        ↓
get_absolute_url()
        ↓
build_absolute_uri()
        ↓
montar assunto
        ↓
montar mensagem
        ↓
send_mail()
        ↓
MAILERS
        ↓
SMTP
        ↓
Gmail
        ↓
destinatário recebe
        ↓
enviado = True
        ↓
share.html
        ↓
mensagem de sucesso
```

---

# 32. Arquivos envolvidos

```text
filmes/
│
├── forms.py
│   └── RecomendarPostForm
│
├── views.py
│   └── recomendar_post
│
├── urls.py
│   └── recomendar_post
│
└── templates/
    └── filmes/
        └── post/
            ├── detail.html
            └── share.html
```

Além disso:

```text
config/settings.py
↓
MAILERS
DEFAULT_FROM_EMAIL

.env
↓
e-mail
senha de app
```

---

# 33. Mapa mental das responsabilidades

## `forms.py`

```text
define campos
valida dados
normaliza dados
```

## `views.py`

```text
recebe GET/POST
processa formulário
monta e-mail
envia e-mail
```

## `urls.py`

```text
define endereço da funcionalidade
```

## `share.html`

```text
mostra formulário
mostra erros
mostra sucesso
```

## `settings.py`

```text
configura envio de e-mail
```

## `.env`

```text
guarda credenciais
```

---

# 34. O que decorar

```python
form = RecomendarPostForm()
```

→ formulário vazio.

```python
form = RecomendarPostForm(request.POST)
```

→ formulário preenchido.

```python
form.is_valid()
```

→ valida.

```python
form.cleaned_data
```

→ pega dados validados.

```python
post.get_absolute_url()
```

→ caminho do post.

```python
request.build_absolute_uri(...)
```

→ URL completa.

```python
send_mail(...)
```

→ envia e-mail.

```django
{{ form.as_p }}
```

→ renderiza o formulário.

```django
{% csrf_token %}
```

→ proteção de POST contra CSRF.

```django
{% url ... %}
```

→ gera URL dinamicamente.

---

# Resumo final

A funcionalidade de recomendação por e-mail conecta várias partes do Django:

```text
Model
+
URL
+
View
+
Form
+
Template
+
Validação
+
CSRF
+
SMTP
+
E-mail
```

A ideia principal é:

```text
usuário envia dados
↓
Django valida
↓
dados validados entram na lógica
↓
Django monta uma mensagem
↓
envia pelo backend de e-mail
↓
template mostra o resultado
```

Essa é uma estrutura que aparece em muitas funcionalidades web além de e-mail, como:

```text
cadastro
login
comentários
checkout
contato
edição de perfil
avaliações
```