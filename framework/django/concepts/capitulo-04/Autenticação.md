# Django — Autenticação, Login, Dashboard e Logout no CinePost

## Objetivo desta etapa

Nesta parte do projeto começamos a transformar o CinePost em um site com contas de usuários.

Construímos:

```text
App de contas
↓
Sistema de autenticação do Django
↓
Login manual para aprendizado
↓
LoginView pronta do Django
↓
Dashboard protegido
↓
Redirecionamentos de login
↓
Logout
```

O objetivo é chegar posteriormente a:

```text
cadastro
perfil
edição de perfil
troca de senha
recuperação de senha
```

---

# 1. Criando o app `contas`

Criamos um app separado:

```powershell
python manage.py startapp contas
```

A estrutura ficou parecida com:

```text
cinepost/
├── config/
├── filmes/
├── contas/
└── manage.py
```

---

# Por que criar outro app?

Queremos separar responsabilidades.

```text
filmes
→ posts
→ comentários
→ tags
→ busca
```

```text
contas
→ login
→ logout
→ cadastro
→ perfil
→ senhas
```

Isso mantém o projeto organizado.

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

Colocamos antes do Admin:

```python
INSTALLED_APPS = [
    "contas.apps.ContasConfig",

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

# Por que `contas` antes do Admin?

O Django procura templates seguindo a ordem de:

```python
INSTALLED_APPS
```

Como vamos substituir alguns templates de autenticação, colocar `contas` antes ajuda o Django a encontrar nossos templates antes dos templates do Admin.

---

# 3. O sistema de autenticação do Django

O Django já possui um sistema completo:

```python
django.contrib.auth
```

Ele fornece recursos como:

```text
User
Group
Permission
Login
Logout
Sessões
Troca de senha
Recuperação de senha
```

---

# 4. O Model `User`

O Django já possui um Model de usuário.

Campos importantes:

```text
username
password
email
first_name
last_name
is_active
is_staff
is_superuser
```

O mesmo `User` é utilizado pelo:

```text
Django Admin
```

e pelo nosso login público.

---

# 5. Sessões

Quando um usuário faz login:

```text
usuário
↓
credenciais válidas
↓
sessão
↓
continua autenticado nas próximas páginas
```

O Django já possui:

```text
SessionMiddleware
```

para trabalhar com sessões.

---

# 6. `AuthenticationMiddleware`

Também temos:

```text
AuthenticationMiddleware
```

Ele associa o usuário da sessão ao:

```python
request.user
```

Por isso podemos fazer:

```python
request.user
```

ou no template:

```django
{{ request.user.username }}
```

---

# PARTE 1 — Login manual

Antes de usar o login pronto do Django, construímos nossa própria view para entender o processo.

---

# 7. Criando `LoginForm`

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

Não estávamos criando um novo usuário.

Só queríamos receber:

```text
username
password
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

# 8. `PasswordInput`

Usamos:

```python
widget=forms.PasswordInput
```

Isso gera aproximadamente:

```html
<input type="password">
```

Então o navegador mostra:

```text
••••••••
```

em vez da senha.

Importante:

```text
PasswordInput não é responsável por criptografar a senha.
```

Ele apenas muda a forma como o campo aparece no navegador.

---

# 9. Criando a view manual

No:

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

# 10. GET

Quando acessávamos:

```text
/contas/login/
```

sem enviar formulário:

```text
GET
```

A view fazia:

```python
form = LoginForm()
```

Fluxo:

```text
GET
↓
form vazio
↓
template
↓
usuário vê login
```

---

# 11. POST

Quando o usuário clicava em:

```text
Entrar
```

o formulário enviava:

```text
POST
```

Então:

```python
form = LoginForm(request.POST)
```

recebia os dados.

---

# 12. `form.is_valid()`

Executávamos:

```python
if form.is_valid():
```

Isso valida os campos.

Depois:

```python
dados = form.cleaned_data
```

---

# 13. `cleaned_data`

Contém os dados já validados.

Exemplo:

```python
dados["username"]
dados["password"]
```

---

# 14. `authenticate()`

A parte principal era:

```python
user = authenticate(
    request,
    username=dados["username"],
    password=dados["password"],
)
```

O Django verifica:

```text
usuário existe?
↓
senha está correta?
```

Se estiver correto:

```text
retorna User
```

Se estiver errado:

```python
None
```

---

# 15. `authenticate()` x `login()`

Essa diferença é muito importante.

## `authenticate()`

```python
authenticate(...)
```

significa:

```text
Confira usuário e senha.
```

Ele ainda não cria a sessão.

Mentalmente:

```text
authenticate()
= conferir identidade
```

---

## `login()`

Depois usamos:

```python
login(request, user)
```

Isso coloca o usuário autenticado na sessão.

Mentalmente:

```text
login()
= permitir entrada e manter autenticado
```

---

# Fluxo

```text
username + senha
↓
authenticate()
↓
User
↓
login()
↓
sessão
```

---

# 16. `is_active`

Também verificamos:

```python
if user.is_active:
```

Um usuário pode existir, mas estar desativado.

```text
is_active = True
→ pode entrar
```

```text
is_active = False
→ conta desativada
```

---

# 17. Template manual

Criamos inicialmente:

```text
contas/templates/contas/login.html
```

Esse template era utilizado somente pela nossa:

```python
user_login()
```

---

# PARTE 2 — Login pronto do Django

Depois de entender o processo manual, passamos a utilizar o sistema pronto.

---

# 18. `django.contrib.auth.urls`

Alteramos:

```text
contas/urls.py
```

para:

```python
from django.urls import include, path

from . import views


app_name = "contas"


urlpatterns = [
    path(
        "",
        include("django.contrib.auth.urls"),
    ),
]
```

---

# O que isso adiciona?

O Django disponibiliza várias URLs automaticamente.

Entre elas:

```text
login/
logout/

password_change/
password_change/done/

password_reset/
password_reset/done/

reset/<uidb64>/<token>/
reset/done/
```

Como nosso app está incluído em:

```text
/contas/
```

temos:

```text
/contas/login/
/contas/logout/
/contas/password_change/
/contas/password_reset/
```

---

# 19. O login manual deixou de ser necessário

Antes:

```text
LoginForm
↓
user_login()
↓
contas/login.html
```

Agora:

```text
AuthenticationForm
↓
LoginView
↓
registration/login.html
```

O Django passou a cuidar internamente de:

```text
formulário
validação
authenticate()
login()
sessão
erros
redirecionamento
```

---

# 20. O código antigo pode ser removido

Como não usamos mais a view manual, podemos remover:

```python
def user_login(...)
```

Também podemos remover:

```python
LoginForm
```

se ele não estiver sendo usado em nenhum outro lugar.

E podemos apagar:

```text
contas/templates/contas/login.html
```

porque a `LoginView` padrão não utiliza esse template.

---

# 21. Template padrão da LoginView

Criamos:

```text
contas/
└── templates/
    └── registration/
        └── login.html
```

O nome:

```text
registration/login.html
```

é importante porque é o template padrão esperado pela `LoginView`.

---

# 22. Template com Bootstrap

Exemplo:

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
                            Entre na sua conta do CinePost
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

# 23. CSRF

Como login usa:

```text
POST
```

incluímos:

```django
{% csrf_token %}
```

Isso protege contra:

```text
Cross-Site Request Forgery
```

---

# 24. O que é `next`?

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

Isso permite devolver o usuário para a página que ele tentou acessar.

Exemplo:

```text
usuário tenta acessar dashboard
↓
não está logado
↓
vai para login
↓
faz login
↓
volta para dashboard
```

---

# PARTE 3 — Dashboard protegido

# 25. Criando o dashboard

No:

```text
contas/views.py
```

criamos:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(
        request,
        "contas/dashboard.html",
    )
```

---

# 26. `@login_required`

Esse decorator protege a view.

```python
@login_required
def dashboard(request):
```

significa:

```text
só permita acessar esta view
se o usuário estiver autenticado
```

---

# Usuário autenticado

```text
/contas/dashboard/
↓
@login_required
↓
autenticado ✅
↓
dashboard
```

---

# Usuário anônimo

```text
/contas/dashboard/
↓
@login_required
↓
não autenticado ❌
↓
redireciona para login
```

---

# 27. Criando a URL do dashboard

Em:

```text
contas/urls.py
```

ficou:

```python
from django.urls import include, path

from . import views


app_name = "contas"


urlpatterns = [
    path(
        "",
        include("django.contrib.auth.urls"),
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
]
```

Resultado:

```text
/contas/dashboard/
```

---

# 28. Template do dashboard

Criamos:

```text
contas/templates/contas/dashboard.html
```

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Minha conta | CinePost
{% endblock %}

{% block content %}

<div class="container py-5">

    <div class="row justify-content-center">

        <div class="col-12 col-lg-8">

            <div class="card bg-black border-secondary shadow">

                <div class="card-body p-4">

                    <h1 class="h3 mb-3">
                        Olá, {{ request.user.username }}!
                    </h1>

                    <p class="text-secondary">
                        Você está autenticado no CinePost.
                    </p>

                    <div class="alert alert-dark border-secondary">

                        <strong>Usuário:</strong>
                        {{ request.user.username }}

                        <br>

                        <strong>E-mail:</strong>
                        {{ request.user.email|default:"Não informado" }}

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}
```

---

# 29. `request.user`

Agora conseguimos acessar o usuário autenticado.

Exemplo:

```django
{{ request.user.username }}
```

Também:

```django
{{ request.user.email }}
```

```django
{{ request.user.first_name }}
```

---

# Como isso funciona?

```text
sessão
↓
AuthenticationMiddleware
↓
request.user
↓
template
```

---

# PARTE 4 — Configuração dos redirecionamentos

# 30. Problema encontrado

Quando testamos:

```text
/contas/dashboard/
```

em janela anônima, o Django tentou redirecionar para:

```text
/accounts/login/
```

Mas nosso login fica em:

```text
/contas/login/
```

Resultado:

```text
404
```

---

# 31. Por que isso aconteceu?

O Django possui um endereço padrão de login:

```text
/accounts/login/
```

Como nosso projeto usa:

```text
/contas/login/
```

precisamos configurar isso.

---

# 32. Configurando no `settings.py`

No final do:

```text
config/settings.py
```

adicionamos:

```python
LOGIN_URL = "contas:login"

LOGIN_REDIRECT_URL = "contas:dashboard"

LOGOUT_REDIRECT_URL = "filmes:post_list"
```

---

# 33. `LOGIN_URL`

```python
LOGIN_URL = "contas:login"
```

Significa:

```text
Quando alguém precisar fazer login,
mande para esta URL.
```

Então:

```text
usuário anônimo
↓
dashboard
↓
@login_required
↓
contas:login
```

---

# 34. `LOGIN_REDIRECT_URL`

```python
LOGIN_REDIRECT_URL = "contas:dashboard"
```

Significa:

```text
Depois de login bem-sucedido,
mande para o dashboard.
```

Isso é utilizado principalmente quando não existe um:

```text
next
```

---

# 35. `LOGOUT_REDIRECT_URL`

```python
LOGOUT_REDIRECT_URL = "filmes:post_list"
```

Significa:

```text
Depois do logout,
mande para a lista de filmes.
```

---

# 36. `next` tem prioridade

Imagine:

```text
usuário tenta abrir:

/contas/dashboard/
```

O Django envia para:

```text
/contas/login/?next=/contas/dashboard/
```

Depois do login:

```text
next
↓
/contas/dashboard/
```

Nesse caso o `next` indica para onde voltar.

---

# Fluxo

```text
Usuário tenta dashboard
↓
não autenticado
↓
LOGIN_URL
↓
/contas/login/
↓
next=/contas/dashboard/
↓
login
↓
dashboard
```

---

# PARTE 5 — Logout

# 37. Logout pronto do Django

Como utilizamos:

```python
include("django.contrib.auth.urls")
```

já temos:

```text
/contas/logout/
```

Não foi necessário criar uma view manual de logout.

---

# 38. Logout deve ser enviado por POST

No Django atual, utilizamos um formulário:

```django
<form
    method="post"
    action="{% url 'contas:logout' %}"
>
    {% csrf_token %}

    <button
        type="submit"
        class="btn btn-outline-danger"
    >
        Sair
    </button>
</form>
```

---

# Por que formulário e não um link simples?

Porque estamos executando uma ação:

```text
encerrar sessão
```

Usamos:

```text
POST
```

em vez de simplesmente acessar uma URL por GET.

---

# 39. Fluxo do logout

```text
Usuário logado
↓
clica em Sair
↓
POST
↓
/contas/logout/
↓
Django encerra sessão
↓
LOGOUT_REDIRECT_URL
↓
/filmes/
```

---

# 40. Testando logout

Sequência:

```text
1. Fazer login

2. Abrir dashboard

3. Clicar em Sair

4. Voltar para lista de filmes

5. Tentar abrir dashboard novamente

6. Django envia para login
```

Assim confirmamos:

```text
login ✅
sessão ✅
proteção ✅
logout ✅
```

---

# 41. Estrutura atual do app

Temos aproximadamente:

```text
contas/
│
├── migrations/
│
├── templates/
│   │
│   ├── contas/
│   │   └── dashboard.html
│   │
│   └── registration/
│       └── login.html
│
├── admin.py
├── apps.py
├── models.py
├── urls.py
└── views.py
```

---

# 42. Fluxo completo atual

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
username + senha

↓
Django autentica

↓
sessão

↓
LOGIN_REDIRECT_URL

↓
/contas/dashboard/

↓
@login_required

↓
request.user

↓
dashboard
```

Depois:

```text
Sair
↓
POST /contas/logout/
↓
sessão encerrada
↓
LOGOUT_REDIRECT_URL
↓
/filmes/
```

---

# 43. Login manual x Login pronto

## Manual

Criamos:

```text
LoginForm
user_login()
authenticate()
is_active
login()
HttpResponse
```

Foi útil para entender:

```text
como funciona internamente
```

---

## Pronto

Agora usamos:

```text
django.contrib.auth.urls
LoginView
AuthenticationForm
LogoutView
```

O Django faz a maior parte da lógica.

Nós cuidamos principalmente de:

```text
templates
Bootstrap
redirecionamentos
dashboard
experiência do usuário
```

---

# 44. Conceitos principais aprendidos

```text
django.contrib.auth
= sistema de autenticação
```

```text
User
= conta de usuário
```

```text
authenticate()
= valida usuário e senha
```

```text
login()
= adiciona usuário à sessão
```

```text
session
= mantém usuário autenticado
```

```text
request.user
= usuário da requisição atual
```

```text
is_active
= conta ativa ou desativada
```

```text
AuthenticationForm
= formulário de login pronto
```

```text
LoginView
= view pronta para login
```

```text
LogoutView
= view pronta para logout
```

```text
django.contrib.auth.urls
= conjunto de URLs prontas
```

```text
@login_required
= protege uma view
```

```text
LOGIN_URL
= página usada quando login é necessário
```

```text
LOGIN_REDIRECT_URL
= destino padrão depois do login
```

```text
LOGOUT_REDIRECT_URL
= destino depois do logout
```

```text
next
= página para onde voltar após autenticar
```

---

# 45. Resumo mental

```text
LOGIN

Usuário
↓
LoginView
↓
AuthenticationForm
↓
authenticate
↓
sessão
↓
request.user
```

---

```text
PROTEÇÃO

/contas/dashboard/
↓
@login_required
↓
está logado?

SIM
→ dashboard

NÃO
→ LOGIN_URL
```

---

```text
LOGOUT

Usuário
↓
Sair
↓
POST
↓
LogoutView
↓
sessão encerrada
↓
LOGOUT_REDIRECT_URL
```

---

# 46. O que já está funcionando

Atualmente temos:

```text
✅ Login

✅ Login com usuário do Django

✅ Sessão autenticada

✅ Dashboard protegido

✅ request.user

✅ Redirecionamento automático para login

✅ next

✅ Redirecionamento após login

✅ Logout

✅ Redirecionamento após logout

✅ Bootstrap nos templates
```

---

# 47. Próximos passos

Agora podemos continuar o sistema de contas com:

```text
troca de senha
↓
recuperação de senha
↓
cadastro
↓
perfil
↓
edição de perfil
↓
upload de foto
```

Com isso, a fundação do sistema de autenticação do CinePost já está funcionando.