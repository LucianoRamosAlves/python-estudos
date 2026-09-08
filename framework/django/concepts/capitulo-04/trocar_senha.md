# Django — Autenticação pronta, Login, Logout e Troca de Senha

## Objetivo desta etapa

Nesta parte do projeto CinePost, começamos utilizando o sistema de autenticação que já vem com o Django.

O fluxo estudado foi:

```text
Login manual
↓
Entender authenticate() e login()
↓
Substituir pelo LoginView do Django
↓
Adicionar LogoutView
↓
Adicionar troca de senha
```

---

# 1. Sistema de autenticação do Django

O Django já possui um sistema completo de autenticação localizado em:

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
Troca de senha
Recuperação de senha
Sessões
```

---

# 2. Middlewares importantes

Dois middlewares trabalham diretamente com autenticação.

## SessionMiddleware

Cuida da sessão do usuário.

```text
Usuário faz login
↓
Django grava informações na sessão
↓
usuário continua autenticado nas próximas requisições
```

---

## AuthenticationMiddleware

Associa o usuário da sessão à requisição atual.

Por isso podemos acessar:

```python
request.user
```

---

# 3. Model User

O Django já possui um Model para usuários.

Principais campos:

```text
username
password
email
first_name
last_name
is_active
```

Também existem:

```text
is_staff
is_superuser
```

---

# 4. Login manual

Primeiro criamos nosso próprio login para entender como a autenticação funciona.

Criamos:

```text
contas/forms.py
```

com:

```python
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )
```

---

# 5. PasswordInput

O:

```python
forms.PasswordInput
```

faz o navegador gerar um campo semelhante a:

```html
<input type="password">
```

Assim a senha aparece como:

```text
••••••••
```

Ele não é responsável por criptografar a senha.

---

# 6. View manual de login

Criamos uma view parecida com:

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
        {"form": form},
    )
```

---

# 7. Fluxo do login manual

Quando acessamos a página:

```text
GET
↓
LoginForm()
↓
formulário vazio
↓
template
```

Quando enviamos:

```text
POST
↓
LoginForm(request.POST)
↓
form.is_valid()
↓
cleaned_data
↓
authenticate()
```

---

# 8. authenticate()

O:

```python
authenticate()
```

verifica:

```text
usuário existe?
↓
senha está correta?
```

Se estiver correto:

```text
retorna um objeto User
```

Se estiver errado:

```python
None
```

---

# 9. login()

Depois utilizamos:

```python
login(request, user)
```

O `login()` coloca o usuário autenticado na sessão.

A diferença principal é:

```text
authenticate()
= verifica quem é o usuário
```

```text
login()
= coloca esse usuário na sessão
```

Fluxo:

```text
username + senha
↓
authenticate()
↓
User
↓
login()
↓
sessão autenticada
```

---

# 10. is_active

Também verificamos:

```python
user.is_active
```

Isso informa se a conta está ativa.

```text
True
→ usuário pode entrar
```

```text
False
→ conta desativada
```

---

# 11. URL do login manual

Inicialmente tínhamos:

```python
from django.urls import path

from . import views


urlpatterns = [
    path(
        "login/",
        views.user_login,
        name="login",
    ),
]
```

Como `contas.urls` está incluído no projeto com:

```python
path(
    "contas/",
    include("contas.urls"),
),
```

a URL final ficou:

```text
/contas/login/
```

---

# 12. Por que fizemos login manual?

Não porque precisamos escrever tudo isso em todo projeto.

Fizemos para aprender:

```text
formulário
↓
POST
↓
validação
↓
authenticate()
↓
User
↓
login()
↓
sessão
```

Depois disso passamos para as ferramentas prontas do Django.

---

# 13. Views prontas de autenticação

O Django possui views prontas em:

```python
django.contrib.auth.views
```

Entre elas:

```text
LoginView
LogoutView

PasswordChangeView
PasswordChangeDoneView

PasswordResetView
PasswordResetDoneView
PasswordResetConfirmView
PasswordResetCompleteView
```

---

# 14. LoginView e LogoutView

Substituímos nosso login manual pelas views prontas.

Em:

```text
contas/urls.py
```

passamos a usar:

```python
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    # Login manual usado durante o aprendizado:
    # path(
    #     "login/",
    #     views.user_login,
    #     name="login",
    # ),

    path(
        "login/",
        auth_views.LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]
```

---

# 15. Antes x agora

Antes:

```text
nosso LoginForm
↓
nossa user_login()
↓
authenticate()
↓
login()
```

Agora:

```text
AuthenticationForm do Django
↓
LoginView
↓
Django cuida da autenticação
```

---

# 16. AuthenticationForm

A `LoginView` utiliza por padrão:

```python
django.contrib.auth.forms.AuthenticationForm
```

Esse formulário já trata:

```text
username
senha
validação
autenticação
erros
```

Por isso não precisamos mais escrever toda a lógica manual.

---

# 17. Pasta registration

As views de autenticação do Django procuram templates dentro de:

```text
registration/
```

Criamos:

```text
contas/
└── templates/
    └── registration/
        ├── login.html
        └── logged_out.html
```

---

# 18. registration/login.html

A `LoginView` procura por padrão:

```text
registration/login.html
```

Um exemplo utilizado no CinePost:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Entrar | CinePost
{% endblock %}

{% block content %}

<div class="container py-5">

    <h1>Entrar</h1>

    {% if form.errors %}

        <div class="alert alert-danger">
            Usuário ou senha inválidos.
        </div>

    {% endif %}

    <form
        action="{% url 'login' %}"
        method="post"
    >

        {{ form.as_p }}

        {% csrf_token %}

        <input
            type="hidden"
            name="next"
            value="{{ next }}"
        >

        <button
            type="submit"
            class="btn btn-danger"
        >
            Entrar
        </button>

    </form>

</div>

{% endblock %}
```

---

# 19. form.errors

A `AuthenticationForm` já gera erros quando a autenticação falha.

Por isso podemos usar:

```django
{% if form.errors %}
```

para mostrar uma mensagem ao usuário.

---

# 20. next

No formulário temos:

```django
<input
    type="hidden"
    name="next"
    value="{{ next }}"
>
```

O `next` guarda uma URL para onde o usuário deve voltar depois de fazer login.

Exemplo:

```text
usuário tenta acessar:

/contas/
```

mas precisa fazer login.

Django pode enviar para:

```text
/contas/login/?next=/contas/
```

Depois:

```text
login bem-sucedido
↓
next
↓
/contas/
```

---

# 21. LogoutView

Criamos:

```python
path(
    "logout/",
    auth_views.LogoutView.as_view(),
    name="logout",
),
```

Resultado:

```text
/contas/logout/
```

A view pronta do Django encerra a sessão.

No Django atual, o logout deve ser executado utilizando:

```text
POST
```

Exemplo:

```django
<form
    action="{% url 'logout' %}"
    method="post"
>
    {% csrf_token %}

    <button type="submit">
        Sair
    </button>
</form>
```

---

# 22. logged_out.html

Criamos:

```text
registration/logged_out.html
```

Essa página pode ser exibida depois que o usuário encerra a sessão.

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Sessão encerrada | CinePost
{% endblock %}

{% block content %}

<h1>Você saiu da sua conta</h1>

<p>
    Sua sessão foi encerrada com sucesso.
</p>

<a href="{% url 'login' %}">
    Entrar novamente
</a>

{% endblock %}
```

---

# 23. INSTALLED_APPS e templates

Colocamos nosso app:

```python
"contas.apps.ContasConfig",
```

antes de:

```python
"django.contrib.admin",
```

Exemplo:

```python
INSTALLED_APPS = [
    "contas.apps.ContasConfig",

    "django.contrib.admin",
    ...
]
```

Isso é importante porque o Django procura templates seguindo a ordem dos apps.

Como o Admin também possui templates dentro de:

```text
registration/
```

queremos que nossos templates sejam encontrados primeiro.

---

# PARTE — TROCA DE SENHA

# 24. Objetivo da troca de senha

Queremos permitir que um usuário que:

```text
já está autenticado
```

consiga trocar a própria senha.

Essa situação é diferente de:

```text
"Esqueci minha senha"
```

Aqui o usuário conhece a senha atual.

---

# 25. Views prontas para troca de senha

O Django fornece:

```python
PasswordChangeView
```

e:

```python
PasswordChangeDoneView
```

---

# PasswordChangeView

Cuida de:

```text
mostrar formulário
↓
receber senha atual
↓
verificar senha
↓
receber nova senha
↓
validar nova senha
↓
salvar nova senha
```

---

# PasswordChangeDoneView

É a página exibida depois que a alteração termina com sucesso.

Fluxo:

```text
PasswordChangeView
↓
senha alterada
↓
PasswordChangeDoneView
```

---

# 26. URLs da troca de senha

Em:

```text
contas/urls.py
```

adicionamos:

```python
path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(),
    name="password_change",
),

path(
    "password-change/done/",
    auth_views.PasswordChangeDoneView.as_view(),
    name="password_change_done",
),
```

O arquivo ficou semelhante a:

```python
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),

    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
```

---

# 27. URLs finais

Como `contas.urls` está incluído usando:

```python
path(
    "contas/",
    include("contas.urls"),
),
```

temos:

```text
/contas/login/

/contas/logout/

/contas/password-change/

/contas/password-change/done/
```

---

# 28. Nome da URL x endereço da URL

É importante distinguir:

```text
password_change_done
```

de:

```text
/contas/password-change/done/
```

O primeiro:

```text
password_change_done
```

é o nome interno da URL.

O segundo:

```text
/contas/password-change/done/
```

é o endereço acessado no navegador.

---

# 29. Por que `name="password_change_done"` é importante?

Depois de alterar a senha, a:

```python
PasswordChangeView
```

procura uma URL chamada:

```text
password_change_done
```

Por isso criamos:

```python
path(
    "password-change/done/",
    auth_views.PasswordChangeDoneView.as_view(),
    name="password_change_done",
),
```

Fluxo:

```text
PasswordChangeView
↓
senha foi alterada
↓
procura password_change_done
↓
encontra a URL
↓
PasswordChangeDoneView
```

---

# 30. Template do formulário

Criamos:

```text
contas/
└── templates/
    └── registration/
        └── password_change_form.html
```

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Alterar senha | CinePost
{% endblock %}

{% block content %}

<div class="container py-5">

    <div class="row justify-content-center">

        <div class="col-12 col-md-7 col-lg-5">

            <div class="card bg-black border-secondary">

                <div class="card-body p-4">

                    <h1 class="h3 mb-3">
                        Alterar senha
                    </h1>

                    <p class="text-secondary">
                        Informe sua senha atual e escolha uma nova senha.
                    </p>

                    <form method="post">

                        {{ form.as_p }}

                        {% csrf_token %}

                        <button
                            type="submit"
                            class="btn btn-danger"
                        >
                            Alterar senha
                        </button>

                    </form>

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}
```

---

# 31. Quem cria esse formulário?

Nós não criamos um `forms.py` para isso.

A própria:

```python
PasswordChangeView
```

já fornece o formulário necessário.

Ele pede:

```text
senha atual

nova senha

confirmação da nova senha
```

---

# 32. CSRF

Como estamos enviando uma alteração através de:

```text
POST
```

precisamos:

```django
{% csrf_token %}
```

---

# 33. Template de sucesso

Criamos:

```text
registration/password_change_done.html
```

Exemplo:

```django
{% extends "filmes/base.html" %}

{% block title %}
    Senha alterada | CinePost
{% endblock %}

{% block content %}

<div class="container py-5">

    <div class="row justify-content-center">

        <div class="col-12 col-md-7 col-lg-5">

            <div class="card bg-black border-secondary">

                <div class="card-body p-4 text-center">

                    <h1 class="h3 mb-3">
                        Senha alterada
                    </h1>

                    <p class="text-secondary">
                        Sua senha foi alterada com sucesso.
                    </p>

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}
```

---

# 34. Fluxo completo da troca de senha

```text
Usuário acessa:

/contas/password-change/

↓
PasswordChangeView

↓
password_change_form.html

↓
senha atual
+
nova senha
+
confirmação

↓
POST

↓
Django verifica senha atual

↓
Django valida nova senha

↓
Django salva nova senha

↓
procura:

password_change_done

↓
PasswordChangeDoneView

↓
password_change_done.html
```

---

# 35. Teste

Para testar:

```text
1. Faça login.

2. Acesse:

/contas/password-change/

3. Digite a senha atual.

4. Digite a nova senha.

5. Confirme a nova senha.

6. Envie o formulário.

7. Veja a página de sucesso.

8. Faça logout.

9. Entre novamente com a nova senha.
```

Se conseguir entrar com a nova senha:

```text
troca de senha funcionando ✅
```

---

# 36. Trocar senha x recuperar senha

São coisas diferentes.

## Troca de senha

Usuário:

```text
está logado
+
sabe a senha atual
```

Usamos:

```text
PasswordChangeView
```

---

## Recuperação de senha

Usuário:

```text
não lembra a senha
```

Então futuramente utilizaremos:

```text
PasswordResetView
PasswordResetDoneView
PasswordResetConfirmView
PasswordResetCompleteView
```

Essa será a próxima etapa.

---

# 37. O que temos até agora

Até esta parte do capítulo aprendemos:

```text
✅ django.contrib.auth

✅ User

✅ sessões

✅ AuthenticationMiddleware

✅ SessionMiddleware

✅ login manual

✅ LoginForm

✅ authenticate()

✅ login()

✅ is_active

✅ LoginView

✅ AuthenticationForm

✅ LogoutView

✅ registration/login.html

✅ registration/logged_out.html

✅ parâmetro next

✅ troca de senha

✅ PasswordChangeView

✅ PasswordChangeDoneView

✅ password_change_form.html

✅ password_change_done.html
```

---

# 38. Resumo mental

## Login manual

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
login()
↓
sessão
```

---

## Login pronto

```text
LoginView
↓
AuthenticationForm
↓
Django autentica
↓
sessão
```

---

## Logout

```text
POST
↓
LogoutView
↓
sessão encerrada
```

---

## Troca de senha

```text
PasswordChangeView
↓
senha atual
↓
nova senha
↓
Django altera
↓
PasswordChangeDoneView
↓
sucesso
```

---

# Próximo assunto

O próximo passo do livro será:

```text
Recuperação de senha esquecida
```

utilizando:

```text
PasswordResetView
PasswordResetDoneView
PasswordResetConfirmView
PasswordResetCompleteView
```

Nesse fluxo teremos:

```text
e-mail
↓
token
↓
link de recuperação
↓
nova senha
```