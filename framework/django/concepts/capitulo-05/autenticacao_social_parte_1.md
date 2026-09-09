# Django 5 by Example — Capítulo 5
## Autenticação Social — Parte 1

# Visão geral do capítulo

No capítulo anterior construímos praticamente toda a base de autenticação do CinePost.

Já temos:

```text
Cadastro
Login
Logout
Troca de senha
Recuperação de senha
Profile
Foto de perfil
Edição da conta
```

Agora o capítulo 5 vai ampliar esse sistema.

A ideia geral será chegar a:

```text
                ┌─ usuário + senha
Usuário ────────┼─ e-mail + senha
                └─ Google
                       ↓
                  autenticação
                       ↓
                   Dashboard
                       ↓
                    Profile
```

---

# O que será estudado no capítulo

O capítulo vai abordar:

```text
Django Messages
Backend personalizado de autenticação
Login usando e-mail
Prevenção de e-mails duplicados
Python Social Auth
OAuth 2.0
HTTPS no desenvolvimento
Login com Google
Pipeline de autenticação social
Criação automática de Profile
```

---

# Autenticação social

Atualmente nosso CinePost possui autenticação tradicional:

```text
username
+
senha
```

O capítulo adicionará autenticação através do Google.

O usuário poderá fazer algo como:

```text
Entrar com Google
```

sem precisar criar uma nova senha específica para o CinePost.

---

# OAuth 2.0

O login com Google utiliza OAuth 2.0.

O CinePost NÃO recebe a senha do Google.

O fluxo é aproximadamente:

```text
CinePost
↓
Entrar com Google
↓
Google
↓
usuário faz login no Google
↓
usuário autoriza o CinePost
↓
Google devolve uma autorização
↓
CinePost identifica o usuário
↓
login realizado
```

A senha permanece com o Google.

```text
Senha Google
→ Google

CinePost
→ recebe apenas as informações/autorização permitidas
```

---

# Python Social Auth

O livro utiliza Python Social Auth.

No Django, será utilizado um pacote relacionado a:

```text
social-auth-app-django
```

Ele ajuda a integrar provedores externos de autenticação, como:

```text
Google
```

Não instalamos ainda.

Quando chegarmos nessa parte, devemos verificar uma versão compatível com:

```text
Python 3.14
Django 6.1
```

em vez de simplesmente copiar a versão usada no livro.

---

# Profile e autenticação social

Hoje nosso cadastro próprio executa:

```python
new_user.save()

Profile.objects.create(
    user=new_user
)
```

Então:

```text
cadastro pelo CinePost
↓
User criado
↓
Profile criado
```

Porém, quando futuramente o usuário entrar pelo Google:

```text
Google
↓
Python Social Auth
↓
User criado
```

esse processo NÃO passa pela nossa função:

```python
register()
```

Portanto poderíamos acabar com:

```text
User ✅
Profile ❌
```

O capítulo ensinará a alterar a pipeline de autenticação social.

O objetivo será:

```text
novo usuário via Google
↓
User criado
↓
pipeline executada
↓
Profile criado
↓
User ↔ Profile
```

---

# Technical requirements

O código original do capítulo possui seu próprio:

```text
requirements.txt
```

O livro diz que podemos instalar tudo de uma vez:

```powershell
python -m pip install -r requirements.txt
```

Porém, no CinePost NÃO vamos fazer isso automaticamente.

Motivo:

```text
Livro
→ Django 5

Nosso ambiente
→ Django 6.1
→ Python 3.14
```

Algumas versões usadas pelo livro podem estar antigas ou incompatíveis.

Nossa estratégia continuará sendo:

```text
chega em uma biblioteca
↓
entendemos para que serve
↓
verificamos compatibilidade
↓
instalamos somente o necessário
```

Provavelmente aparecerão bibliotecas como:

```text
social-auth-app-django
django-extensions
```

Mas ainda não instalamos nenhuma delas nesta parte.

---

# Django Messages Framework

O primeiro assunto prático do capítulo é:

```python
django.contrib.messages
```

O Messages Framework serve para mostrar mensagens temporárias ao usuário.

Exemplo:

```text
Usuário edita perfil
↓
dados são salvos
↓
"Perfil atualizado com sucesso."
```

Outro exemplo:

```text
formulário possui erro
↓
"Não foi possível atualizar o perfil."
```

---

# Mensagens temporárias

Messages são notificações de uma única utilização.

Fluxo:

```text
View cria mensagem
↓
próxima página recebe mensagem
↓
template exibe
↓
mensagem é consumida
```

Exemplo:

```python
messages.success(
    request,
    "Perfil atualizado com sucesso.",
)
```

Depois:

```text
redirect
↓
próxima requisição
↓
mensagem aparece
↓
depois desaparece
```

---

# Onde as mensagens são armazenadas?

Por padrão, o Django utiliza armazenamento baseado em cookie, com fallback para sessão quando necessário.

Não precisamos criar uma tabela específica para essas mensagens.

Elas são feitas para informações temporárias.

Exemplo:

```text
"Perfil atualizado."
```

não precisa permanecer no banco de dados.

---

# Tipos de mensagens

O Django possui atalhos para diferentes níveis.

## Success

```python
messages.success(
    request,
    "Operação realizada com sucesso.",
)
```

Usado quando algo funcionou.

Exemplo:

```text
Perfil atualizado com sucesso.
```

---

## Info

```python
messages.info(
    request,
    "Informação importante.",
)
```

Usado para informações gerais.

---

## Warning

```python
messages.warning(
    request,
    "Atenção.",
)
```

Usado quando ainda não ocorreu necessariamente um erro, mas existe algo importante para avisar.

---

## Error

```python
messages.error(
    request,
    "Não foi possível realizar a operação.",
)
```

Usado quando algo falhou.

---

## Debug

```python
messages.debug(
    request,
    "Informação de depuração.",
)
```

Usado principalmente durante desenvolvimento.

---

# Infraestrutura do Messages no CinePost

Nosso projeto já veio praticamente pronto para utilizar Messages.

No `settings.py` já existe:

```python
"django.contrib.messages",
```

em:

```python
INSTALLED_APPS
```

Também existe:

```python
"django.contrib.messages.middleware.MessageMiddleware",
```

em:

```python
MIDDLEWARE
```

E temos:

```python
"django.contrib.messages.context_processors.messages",
```

nos context processors.

Portanto:

```text
Messages Framework
→ já estava ativado
```

Não precisamos instalar nada.

---

# Context Processor

O livro apresenta o conceito de context processor.

Um context processor é uma função que recebe:

```text
request
```

e adiciona informações automaticamente ao contexto dos templates.

No caso do Messages Framework:

```python
django.contrib.messages.context_processors.messages
```

adiciona a variável:

```django
messages
```

aos templates.

Por isso podemos simplesmente fazer:

```django
{% if messages %}
```

sem passar `messages` manualmente em cada view.

---

# Messages no base.html

Como queremos mostrar mensagens em qualquer página do CinePost, utilizamos o:

```text
filmes/base.html
```

Assim:

```text
qualquer view
↓
gera mensagem
↓
qualquer página que herda base.html
↓
consegue mostrar mensagem
```

No `base.html`, antes do:

```django
{% block content %}
```

adicionamos uma área para mensagens.

Estrutura:

```django
{% if messages %}

    {% for message in messages %}

        ...

    {% endfor %}

{% endif %}
```

---

# Messages + Bootstrap

Como o CinePost utiliza Bootstrap, usamos os alerts.

Para sucesso:

```html
alert-success
```

Para erro:

```html
alert-danger
```

Para aviso:

```html
alert-warning
```

Para informação:

```html
alert-info
```

---

# Exemplo de mensagem de sucesso

```django
{% if message.tags == "success" %}

    <div
        class="alert alert-success alert-dismissible fade show"
        role="alert"
    >

        {{ message }}

        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Fechar"
        ></button>

    </div>

{% endif %}
```

Como nosso `base.html` já carrega:

```text
bootstrap.bundle.min.js
```

o botão de fechar o alerta funciona.

---

# message.tags

Cada mensagem possui uma tag.

Exemplo:

```python
messages.success(...)
```

gera:

```text
success
```

Então podemos verificar:

```django
{% if message.tags == "success" %}
```

Da mesma forma:

```text
messages.error()
→ error

messages.warning()
→ warning

messages.info()
→ info
```

---

# Não utilizamos |safe

O exemplo do livro possui:

```django
{{ message|safe }}
```

No CinePost preferimos:

```django
{{ message }}
```

porque assim o Django continua escapando HTML automaticamente.

Isso é mais seguro.

Só devemos utilizar:

```django
|safe
```

quando realmente quisermos permitir HTML e tivermos certeza de que o conteúdo é confiável.

---

# Messages na view edit()

Importamos:

```python
from django.contrib import messages
```

Nossa view:

```python
edit()
```

agora pode gerar mensagens.

---

# Mensagem de sucesso

Quando os dois formulários estão válidos:

```python
if user_form.is_valid() and profile_form.is_valid():

    user_form.save()
    profile_form.save()

    messages.success(
        request,
        "Perfil atualizado com sucesso.",
    )

    return redirect("edit")
```

Fluxo:

```text
POST
↓
UserEditForm válido
+
ProfileEditForm válido
↓
salva User
↓
salva Profile
↓
messages.success()
↓
redirect("edit")
```

---

# Mensagem de erro

Caso um dos formulários seja inválido:

```python
else:
    messages.error(
        request,
        "Não foi possível atualizar o perfil. Verifique os campos.",
    )
```

Fluxo:

```text
POST
↓
algum formulário inválido
↓
não salva
↓
messages.error()
↓
template mostra os erros
```

---

# POST + Redirect + GET

Agora nossa edição segue um padrão muito importante:

```text
POST
↓
salvar
↓
redirect
↓
GET
```

Também chamado conceitualmente de:

```text
Post/Redirect/Get
```

Isso evita problemas como reenviar o formulário ao atualizar a página.

---

# Fluxo completo com Messages

```text
Usuário acessa /contas/edit/
↓
GET
↓
formulários aparecem
↓
usuário altera os dados
↓
POST
↓
validação
```

Se estiver válido:

```text
save()
↓
messages.success()
↓
redirect("edit")
↓
GET
↓
base.html
↓
"Perfil atualizado com sucesso."
```

Se estiver inválido:

```text
messages.error()
↓
renderiza formulário
↓
mensagem de erro
+
erros específicos dos campos
```

---

# Por que colocar Messages no base.html?

Porque o sistema é global.

Não precisamos repetir código de mensagem em:

```text
edit.html
register.html
detail.html
share.html
etc.
```

Todas essas páginas herdam:

```django
{% extends "filmes/base.html" %}
```

Então:

```text
base.html
→ ponto central das mensagens
```

---

# Possibilidades futuras

Agora podemos futuramente utilizar:

```python
messages.success(
    request,
    "Comentário adicionado com sucesso.",
)
```

ou:

```python
messages.success(
    request,
    "Conta criada com sucesso.",
)
```

ou:

```python
messages.error(
    request,
    "Não foi possível enviar o e-mail.",
)
```

sem precisar criar uma página de confirmação exclusiva para cada operação.

---

# Estado atual do CinePost

Antes:

```text
Editar perfil
↓
salvar
↓
página simplesmente recarregava/redirecionava
```

Agora:

```text
Editar perfil
↓
salvar
↓
redirect
↓
feedback visual
```

Exemplo:

```text
✅ Perfil atualizado com sucesso.
```

ou:

```text
❌ Não foi possível atualizar o perfil.
```

---

# Resumo mental

## Messages

```text
View
↓
messages.success/error/etc.
↓
próxima requisição
↓
base.html
↓
mensagem aparece
↓
mensagem é removida
```

---

## Tipos

```text
success
→ sucesso

info
→ informação

warning
→ aviso

error
→ falha

debug
→ depuração
```

---

## Infraestrutura

```text
django.contrib.messages
+
MessageMiddleware
+
messages context processor
+
base.html
```

---

# O que vem a seguir

A próxima parte do capítulo será:

```text
Custom Authentication Backend
```

O objetivo será permitir que o usuário faça login usando:

```text
e-mail
+
senha
```

além do sistema tradicional baseado em:

```text
username
+
senha
```

Depois disso o capítulo avançará para:

```text
e-mail único
↓
OAuth 2.0
↓
Python Social Auth
↓
HTTPS local
↓
Google Login
↓
pipeline
↓
Profile automático
```

---

# Estado do capítulo até aqui

```text
Introdução ao capítulo             ✅
OAuth 2.0 explicado                ✅
Python Social Auth apresentado     ✅
Technical requirements             ✅
Estratégia de dependências          ✅
Django Messages                    ✅
Tipos de mensagens                 ✅
Context processor                  ✅
Messages no base.html              ✅
Messages na edit()                 ✅
Post/Redirect/Get                  ✅

Backend de autenticação por e-mail ⏳ próximo
Google OAuth                        ⏳
HTTPS local                         ⏳
Pipeline social                     ⏳
Profile social automático           ⏳
```