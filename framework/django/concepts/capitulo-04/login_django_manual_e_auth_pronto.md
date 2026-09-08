# Django — Login Manual e Sistema de Autenticação Pronto

## Objetivo

Neste estudo aprendemos duas formas de fazer login no Django.

Primeiro:

```text
Login manual
```

para entender o funcionamento interno.

Depois:

```text
LoginView pronta do Django
```

que é a abordagem que vamos manter no projeto.

O aprendizado foi:

```text
entender como funciona
↓
depois usar a solução pronta do framework
```

---

# PARTE 1 — Login Manual

# 1. Criando o app de contas

Criamos:

```powershell
python manage.py startapp contas
```

A responsabilidade desse app é:

```text
login
logout
cadastro
senha
perfil
```

Enquanto:

```text
filmes
```

continua responsável por:

```text
posts
comentários
tags
busca
```

---

# 2. Registrando o app

No:

```text
config/settings.py
```

adicionamos:

```python
"contas.apps.ContasConfig",
```

Neste estudo colocamos o app antes do Admin:

```python
INSTALLED_APPS = [
    "contas.apps.ContasConfig",

    "django.contrib.admin",
    "django.contrib.auth",
    ...
]
```

Isso também é útil porque posteriormente vamos sobrescrever templates de autenticação fornecidos pelo Django.

---

# 3. O sistema de autenticação do Django

O Django já possui:

```python
django.contrib.auth
```

Ele fornece:

```text
User
Group
Permission

login
logout
autenticação
sessões
troca de senha
recuperação de senha
```

---

# 4. Model `User`

O Django possui um Model de usuário.

Entre os principais campos:

```text
username
password
email
first_name
last_name
is_active
```

Esse mesmo sistema já é utilizado pelo:

```text
/admin/
```

---

# 5. Sessões e autenticação

Dois middlewares importantes já vêm configurados.

## `SessionMiddleware`

Cuida da sessão.

```text
usuário entra
↓
Django cria/usa sessão
↓
usuário continua autenticado entre páginas
```

---

## `AuthenticationMiddleware`

Associa o usuário da sessão ao:

```python
request
```

Por isso podemos posteriormente usar:

```python
request.user
```

---

# Exemplo

```python
request.user.username
```

ou:

```python
request.user.is_authenticated
```

---

# 6. Criando o formulário manual

Criamos:

```text
contas/forms.py
```

Com:

```python
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
    )
```

---

# Por que `forms.Form`?

Não estamos criando um usuário.

Estamos apenas recebendo:

```text
username
password
```

para verificar uma conta existente.

Portanto usamos:

```python
forms.Form
```

e não:

```python
forms.ModelForm
```

---

# 7. `PasswordInput`

Usamos:

```python
widget=forms.PasswordInput
```

Isso produz aproximadamente:

```html
<input type="password">
```

No navegador:

```text
••••••••
```

Importante:

```text
PasswordInput não criptografa a senha.
```

Ele apenas informa ao navegador que aquele campo representa uma senha.

A validação real é feita pelo sistema de autenticação do Django.

---

# 8. Criando a view manual

Em:

```text
contas/views.py
```

criamos:

```python
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            dados = form.cleaned_data

            user = authenticate(
                request,
                username=dados["username"],
                password=dados["password"],
            )

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponse(
                        "Autenticado com sucesso."
                    )

                return HttpResponse(
                    "Conta desativada."
                )

            return HttpResponse(
                "Usuário ou senha inválidos."
            )

    else:
        form = LoginForm()

    return render(
        request,
        "contas/login.html",
        {
            "form": form,
        },
    )
```

---

# 9. GET

Quando acessamos:

```text
/contas/login/
```

pela primeira vez, normalmente temos:

```text
GET
```

Então:

```python
form = LoginForm()
```

Cria um formulário vazio.

Fluxo:

```text
GET
↓
LoginForm vazio
↓
template
↓
usuário vê formulário
```

---

# 10. POST

Quando o usuário clica:

```text
Entrar
```

o formulário envia:

```text
POST
```

Então fazemos:

```python
form = LoginForm(request.POST)
```

Agora o formulário contém os valores enviados.

---

# 11. `form.is_valid()`

Executamos:

```python
if form.is_valid():
```

O Django valida os campos.

Por exemplo:

```text
username preenchido?
password preenchido?
```

---

# 12. `cleaned_data`

Depois:

```python
dados = form.cleaned_data
```

Podemos acessar:

```python
dados["username"]
dados["password"]
```

`cleaned_data` contém os dados já validados pelo formulário.

---

# 13. `authenticate()`

Executamos:

```python
user = authenticate(
    request,
    username=dados["username"],
    password=dados["password"],
)
```

Essa é uma das partes mais importantes.

O Django verifica:

```text
usuário existe?
↓
senha está correta?
```

Se estiver correto:

```text
retorna um User
```

Se estiver errado:

```python
None
```

---

# 14. `authenticate()` NÃO faz login

Isso é fundamental.

```python
authenticate()
```

apenas verifica as credenciais.

Mentalmente:

```text
authenticate()
= conferir identidade
```

---

# 15. `user.is_active`

Depois verificamos:

```python
if user.is_active:
```

Um usuário pode existir, mas estar desativado.

Exemplo:

```text
is_active = False
```

Nesse caso não permitimos acesso.

---

# 16. `login()`

Depois de autenticar:

```python
login(request, user)
```

Isso coloca o usuário na sessão atual.

Mentalmente:

```text
authenticate()
= confirmar quem é
```

```text
login()
= colocar na sessão
```

---

# Fluxo manual completo

```text
Usuário
↓
LoginForm
↓
POST
↓
form.is_valid()
↓
cleaned_data
↓
authenticate()
↓
User ou None
↓
is_active
↓
login()
↓
sessão autenticada
```

---

# 17. Criando a URL manual

Criamos:

```text
contas/urls.py
```

Com:

```python
from django.urls import path

from . import views


app_name = "contas"


urlpatterns = [
    path(
        "login/",
        views.user_login,
        name="login",
    ),
]
```

---

# 18. Incluindo no projeto

No:

```text
config/urls.py
```

adicionamos:

```python
path(
    "contas/",
    include("contas.urls"),
),
```

Resultado:

```text
/contas/login/
```

---

# 19. Template manual

Criamos inicialmente:

```text
contas/
└── templates/
    └── contas/
        └── login.html
```

Esse template pertencia à nossa:

```python
user_login()
```

---

# 20. CSRF

Como o formulário usa:

```html
<form method="post">
```

precisamos:

```django
{% csrf_token %}
```

Exemplo:

```django
<form method="post">

    {% csrf_token %}

    ...

</form>
```

Isso protege contra:

```text
Cross-Site Request Forgery
```

---

# PARTE 2 — Login pronto do Django

# 21. Por que fizemos login manual primeiro?

Para entender:

```text
GET
POST
form
cleaned_data
authenticate
is_active
login
session
```

Mas não precisamos reconstruir tudo isso em todos os projetos.

O Django já fornece views prontas.

---

# 22. `django.contrib.auth.urls`

Alteramos:

```text
contas/urls.py
```

para:

```python
from django.urls import include, path


app_name = "contas"


urlpatterns = [
    path(
        "",
        include("django.contrib.auth.urls"),
    ),
]
```

---

# 23. O que isso faz?

Essa única linha:

```python
include("django.contrib.auth.urls")
```

adiciona várias funcionalidades.

Entre elas:

```text
login
logout

password_change
password_change_done

password_reset
password_reset_done

password_reset_confirm
password_reset_complete
```

---

# URLs resultantes

Como nosso app está incluído em:

```text
/contas/
```

temos endereços semelhantes a:

```text
/contas/login/

/contas/logout/

/contas/password_change/

/contas/password_change/done/

/contas/password_reset/

/contas/password_reset/done/
```

---

# 24. Login manual x LoginView

## Antes

Nós mesmos fazíamos:

```python
authenticate()
login()
```

---

## Agora

O Django faz internamente.

Mentalmente:

```text
/contas/login/
↓
LoginView
↓
AuthenticationForm
↓
authenticate()
↓
login()
↓
session
```

---

# 25. `AuthenticationForm`

Antes tínhamos nosso:

```python
LoginForm
```

Agora o Django fornece seu próprio formulário de autenticação:

```text
AuthenticationForm
```

Ele cuida de:

```text
username
password
validação
autenticação
erros
```

---

# 26. Template esperado pela `LoginView`

A view pronta procura:

```text
registration/login.html
```

Portanto criamos:

```text
contas/
└── templates/
    └── registration/
        └── login.html
```

---

# 27. Importante

O antigo:

```text
contas/templates/contas/login.html
```

não é mais utilizado pela LoginView padrão.

Ele existia apenas para:

```python
user_login()
```

---

# 28. O código manual pode ser removido

Depois que entendemos o funcionamento e adotamos a LoginView do Django, podemos apagar:

```python
def user_login(...):
```

E também nosso:

```python
LoginForm
```

caso ele não seja usado em outro lugar.

---

# Antes

```text
LoginForm nosso
↓
user_login()
↓
contas/login.html
```

---

# Agora

```text
AuthenticationForm do Django
↓
LoginView do Django
↓
registration/login.html
```

---

# 29. Template da LoginView

Exemplo com Bootstrap:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Entrar | CinePost
{% endblock %}

{% block content %}

<div class="container py-5">

    <div class="row justify-content-center">

        <div class="col-12 col-md-7 col-lg-5">

            <div class="card bg-black border-secondary shadow">

                <div class="card-body p-4">

                    <div class="text-center mb-4">

                        <h1 class="h3">
                            Entrar
                        </h1>

                        <p class="text-secondary">
                            Entre na sua conta
                        </p>

                    </div>

                    {% if form.errors %}

                        <div class="alert alert-danger">
                            Usuário ou senha inválidos.
                        </div>

                    {% endif %}

                    <form method="post">

                        {% csrf_token %}

                        <div class="mb-3">

                            <label
                                for="{{ form.username.id_for_label }}"
                                class="form-label"
                            >
                                Usuário
                            </label>

                            {{ form.username }}

                        </div>

                        <div class="mb-4">

                            <label
                                for="{{ form.password.id_for_label }}"
                                class="form-label"
                            >
                                Senha
                            </label>

                            {{ form.password }}

                        </div>

                        {% if next %}

                            <input
                                type="hidden"
                                name="next"
                                value="{{ next }}"
                            >

                        {% endif %}

                        <div class="d-grid">

                            <button
                                type="submit"
                                class="btn btn-danger"
                            >
                                Entrar
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}
```

---

# 30. `form.errors`

A view pronta entrega os erros no próprio formulário.

Podemos verificar:

```django
{% if form.errors %}
```

E mostrar:

```text
Usuário ou senha inválidos.
```

---

# 31. O que é `next`?

Essa é uma funcionalidade muito importante.

Imagine que o usuário tente acessar:

```text
/contas/dashboard/
```

sem estar autenticado.

O Django poderá mandar para:

```text
/contas/login/?next=/contas/dashboard/
```

O:

```text
next
```

guarda a página que o usuário queria acessar.

---

# Depois do login

```text
usuário tenta abrir dashboard
↓
não está autenticado
↓
vai para login
↓
faz login
↓
Django lê next
↓
volta para dashboard
```

---

# Campo escondido

No template usamos:

```django
{% if next %}

    <input
        type="hidden"
        name="next"
        value="{{ next }}"
    >

{% endif %}
```

Assim o valor continua disponível depois do POST.

---

# 32. O usuário do Admin também funciona

O login público e o Admin utilizam o mesmo sistema:

```python
django.contrib.auth
```

Portanto um usuário válido no:

```text
/admin/
```

também pode autenticar na nossa LoginView, desde que esteja ativo.

---

# 33. Superuser x usuário comum

O sistema de autenticação é o mesmo.

Podemos ter:

```text
superuser
```

e:

```text
usuário comum
```

Ambos são:

```text
User
```

A diferença está nas permissões.

---

# 34. O que acontece depois de login válido?

Por padrão, se não configurarmos destino e não existir `next`, a LoginView pode tentar redirecionar para uma URL padrão.

Por isso podemos futuramente configurar no:

```text
settings.py
```

algo como:

```python
LOGIN_REDIRECT_URL = "/"
```

ou uma página de dashboard.

Essa parte será configurada quando criarmos nosso dashboard.

---

# 35. Qual abordagem manter?

Para projetos reais, normalmente:

```text
views prontas do Django
```

são melhores do que reimplementar autenticação básica.

Porque já lidam corretamente com várias partes do processo.

Então:

```text
manual
→ importante para aprender
```

```text
django.contrib.auth
→ abordagem que vamos manter
```

---

# 36. Principal diferença

## Login manual

Nós escrevemos:

```text
form
authenticate
is_active
login
erros
```

---

## LoginView

O Django já implementa:

```text
form
authenticate
sessão
validação
erros
redirecionamentos
```

Nós personalizamos principalmente:

```text
template
visual
URLs
configurações
```

---

# 37. Fluxo final atual

```text
Usuário acessa:

/contas/login/

↓
django.contrib.auth.urls

↓
LoginView

↓
AuthenticationForm

↓
usuário envia username + senha

↓
Django autentica

↓
sessão criada

↓
request.user passa a representar
o usuário autenticado
```

---

# 38. Estrutura atual

```text
contas/
│
├── migrations/
│
├── templates/
│   └── registration/
│       └── login.html
│
├── admin.py
├── apps.py
├── models.py
├── urls.py
└── views.py
```

Nosso login manual pode ser removido depois do aprendizado.

---

# 39. Conceitos principais

```text
django.contrib.auth
= sistema de autenticação do Django
```

```text
User
= conta do usuário
```

```text
SessionMiddleware
= gerencia sessão
```

```text
AuthenticationMiddleware
= disponibiliza request.user
```

```text
authenticate()
= verifica credenciais
```

```text
login()
= coloca usuário na sessão
```

```text
is_active
= informa se a conta está habilitada
```

```text
request.user
= usuário associado à requisição atual
```

```text
AuthenticationForm
= formulário pronto do Django
```

```text
LoginView
= view pronta para login
```

```text
django.contrib.auth.urls
= conjunto de URLs prontas de autenticação
```

```text
registration/login.html
= template padrão procurado pela LoginView
```

```text
next
= URL para onde retornar depois do login
```

---

# 40. Resumo mental final

Primeiro aprendemos:

```text
LoginForm
↓
POST
↓
is_valid()
↓
cleaned_data
↓
authenticate()
↓
User
↓
is_active
↓
login()
↓
sessão
```

Depois substituímos por:

```text
django.contrib.auth.urls
↓
LoginView
↓
AuthenticationForm
↓
Django faz todo o processo
↓
registration/login.html
```

A etapa manual mostrou:

```text
como o login funciona
```

A etapa pronta mostrou:

```text
como devemos aproveitar o framework
```

Essa é uma ideia recorrente no Django:

```text
entender o mecanismo
↓
usar as ferramentas prontas
↓
personalizar apenas o necessário
```