# Django — Autenticação com Google OAuth 2.0 no CinePost

## Objetivo

Nesta etapa adicionamos ao CinePost a possibilidade de o usuário entrar no site usando sua conta Google.

Antes tínhamos apenas formas tradicionais de autenticação, como:

```text
username + senha
```

ou:

```text
e-mail + senha
```

Agora adicionamos:

```text
Entrar com Google
```

O fluxo ficou:

```text
Usuário
↓
Clica em "Entrar com Google"
↓
Google confirma a identidade
↓
Google retorna para o Django
↓
Python Social Auth processa os dados
↓
User é localizado ou criado
↓
Profile é criado se necessário
↓
usuário fica autenticado
```

---

# 1. O que é OAuth 2.0?

OAuth 2.0 é um protocolo usado para permitir que um aplicativo utilize um provedor externo para autenticação e autorização.

No nosso caso:

```text
CinePost
↓
Google OAuth 2.0
↓
Conta Google
```

O CinePost não precisa receber a senha do Gmail do usuário.

Quem verifica a identidade é o:

```text
Google
```

Depois o Google informa ao CinePost que aquela pessoa foi autenticada.

---

# 2. Grande vantagem

Sem Google:

```text
Usuário cria username
↓
cria senha
↓
Django guarda hash da senha
↓
faz login
```

Com Google:

```text
Usuário escolhe sua conta Google
↓
Google autentica
↓
CinePost recebe a confirmação
↓
login realizado
```

O usuário não precisa criar uma nova senha específica para o CinePost.

---

# 3. Biblioteca usada

Utilizamos:

```text
social-auth-app-django
```

Instalação:

```powershell
pip install social-auth-app-django
```

Essa biblioteca integra Django ao:

```text
Python Social Auth
```

---

# 4. Adicionando `social_django`

No:

```text
config/settings.py
```

adicionamos:

```python
"social_django",
```

ao:

```python
INSTALLED_APPS
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

    "social_django",

    "taggit",

    "filmes.apps.FilmesConfig",
    "contas.apps.ContasConfig",
]
```

---

# 5. Aplicando migrations

Depois de adicionar `social_django`, executamos:

```powershell
python manage.py migrate
```

Isso criou tabelas utilizadas pelo Python Social Auth.

No Admin apareceu uma nova seção:

```text
PYTHON SOCIAL AUTH
```

com itens como:

```text
Associations
Nonces
User social auths
```

---

# 6. Configurando os backends

No `settings.py` configuramos:

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "contas.authentication.EmailAuthBackend",
    "social_core.backends.google.GoogleOAuth2",
]
```

---

# O que são backends?

São formas diferentes pelas quais o Django pode tentar autenticar um usuário.

Agora temos:

```text
ModelBackend
→ login tradicional do Django
```

```text
EmailAuthBackend
→ nosso login por e-mail
```

```text
GoogleOAuth2
→ login usando Google
```

Mentalmente:

```text
Login
↓
Django verifica os backends
↓
tradicional / e-mail / Google
```

---

# 7. Nome correto do nosso app

O livro utilizava:

```text
account
```

Mas no CinePost nosso app se chama:

```text
contas
```

Por isso não podemos copiar literalmente:

```python
"account.authentication.EmailAuthBackend"
```

No nosso projeto o correto é:

```python
"contas.authentication.EmailAuthBackend"
```

O mesmo vale para:

```python
"contas.authentication.create_profile"
```

---

# 8. Criando o projeto no Google Cloud

No Google Cloud criamos um projeto para o CinePost.

Depois configuramos:

```text
Google Auth Platform
```

e criamos um cliente OAuth.

Tipo escolhido:

```text
Web application
```

Nome:

```text
CinePost
```

---

# 9. Client ID e Client Secret

Depois de criar o cliente, o Google fornece:

```text
Client ID
```

e:

```text
Client Secret
```

O Client ID normalmente possui um formato semelhante a:

```text
123456789-xxxxxxxx.apps.googleusercontent.com
```

Importante:

O Client ID NÃO começa com:

```text
https://
```

Errado:

```text
https://123456....
```

Certo:

```text
123456....apps.googleusercontent.com
```

---

# 10. Client ID x Client Secret

```text
Client ID
→ identifica nossa aplicação
```

```text
Client Secret
→ segredo usado para provar que a aplicação é realmente aquela
```

O Client Secret nunca deve ser:

```text
publicado no GitHub
enviado para outras pessoas
colocado diretamente no código
```

---

# 11. Guardando as credenciais no `.env`

Como o CinePost já utiliza `os.environ`, mantivemos o mesmo padrão.

No `.env`:

```env
CINEPOST_GOOGLE_OAUTH2_KEY=SEU_CLIENT_ID
CINEPOST_GOOGLE_OAUTH2_SECRET=SEU_CLIENT_SECRET
```

Não colocar:

```text
https://
```

no Client ID.

---

# 12. Lendo as credenciais no `settings.py`

No `settings.py`:

```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ[
    "CINEPOST_GOOGLE_OAUTH2_KEY"
]

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ[
    "CINEPOST_GOOGLE_OAUTH2_SECRET"
]
```

Mantivemos o mesmo estilo que já utilizávamos para:

```python
EMAIL_USER = os.environ["CINEPOST_EMAIL_USER"]

EMAIL_PASSWORD = os.environ["CINEPOST_EMAIL_PASSWORD"]
```

---

# 13. Por que usar `.env`?

Para separar:

```text
configuração sensível
```

do:

```text
código-fonte
```

Então o código pode ir para GitHub enquanto:

```text
senha
Client Secret
SECRET_KEY
credenciais do banco
```

ficam fora.

---

# 14. `.gitignore`

O `.env` deve estar no:

```text
.gitignore
```

Exemplo:

```gitignore
.env
```

---

# 15. Configurando as URLs do Social Auth

No:

```text
config/urls.py
```

adicionamos:

```python
path(
    "social-auth/",
    include(
        "social_django.urls",
        namespace="social",
    ),
),
```

Isso adiciona URLs utilizadas pelo Python Social Auth.

---

# 16. URL de início do Google

O Python Social Auth cria uma rota semelhante a:

```text
/social-auth/login/google-oauth2/
```

Ela inicia o processo de autenticação.

---

# 17. URL de retorno

Depois que o usuário autentica no Google, o Google retorna para:

```text
/social-auth/complete/google-oauth2/
```

No nosso ambiente local:

```text
http://localhost:8000/social-auth/complete/google-oauth2/
```

---

# 18. Redirect URI no Google Cloud

No cliente OAuth do Google cadastramos:

```text
http://localhost:8000/social-auth/complete/google-oauth2/
```

Esse endereço precisa ser exatamente igual ao utilizado pelo Django.

Diferenças pequenas podem causar erro.

Por exemplo:

```text
localhost
```

não é necessariamente tratado da mesma forma que:

```text
127.0.0.1
```

E:

```text
http
```

é diferente de:

```text
https
```

---

# 19. Manter tudo consistente

Durante o desenvolvimento usamos:

```text
http://localhost:8000
```

Então usamos também:

```text
http://localhost:8000/social-auth/complete/google-oauth2/
```

Evitar misturar:

```text
localhost
127.0.0.1
http
https
```

sem necessidade.

---

# 20. Botão "Entrar com Google"

O livro utilizava algo parecido com:

```django
<a href="{% url 'social:begin' 'google-oauth2' %}">
    Entrar com Google
</a>
```

Porém, na versão atual da biblioteca, a rota de início exige:

```text
POST
```

e não GET.

---

# 21. Erro 405 que encontramos

Ao usar apenas:

```django
<a href="...">
```

recebemos:

```text
HTTP ERROR 405
```

Isso aconteceu porque:

```text
<a>
→ faz GET
```

enquanto a versão atual do Social Auth espera:

```text
POST
```

---

# 22. Forma correta atual

Trocamos o link por um formulário:

```django
<form
    method="post"
    action="{% url 'social:begin' 'google-oauth2' %}"
>
    {% csrf_token %}

    <button
        type="submit"
        class="btn btn-light"
    >
        Entrar com Google
    </button>
</form>
```

---

# 23. Por que `{% csrf_token %}`?

Como agora estamos enviando:

```text
POST
```

o Django exige proteção CSRF.

Então usamos:

```django
{% csrf_token %}
```

---

# 24. Fluxo correto do botão

```text
Usuário clica
↓
POST
↓
social:begin
↓
Python Social Auth
↓
cria state
↓
redireciona ao Google
```

---

# 25. O que é `state`?

O OAuth utiliza um parâmetro chamado:

```text
state
```

Ele ajuda a proteger o fluxo de autenticação e relacionar:

```text
pedido iniciado
```

com:

```text
resposta recebida
```

---

# 26. Erro `Missing needed parameter state`

Recebemos:

```text
AuthMissingParameter

Missing needed parameter state
```

porque a URL:

```text
/social-auth/complete/google-oauth2/
```

foi acessada diretamente.

Essa URL não é uma página que o usuário deve abrir manualmente.

Ela é o:

```text
callback
```

do Google.

---

# 27. Fluxo correto

Não fazemos:

```text
usuário
↓
/social-auth/complete/google-oauth2/
```

Fazemos:

```text
/login/
↓
Entrar com Google
↓
social:begin
↓
Google
↓
Google retorna para:
complete/google-oauth2/
```

---

# 28. Erro `invalid_client`

Também encontramos:

```text
Error 401
invalid_client
```

O Google informou:

```text
OAuth client was not found
```

O problema estava no Client ID.

Ele havia sido colocado com:

```text
https://
```

no início.

---

# 29. Client ID correto

No `.env`:

```env
CINEPOST_GOOGLE_OAUTH2_KEY=123456789-xxxx.apps.googleusercontent.com
```

Não:

```env
CINEPOST_GOOGLE_OAUTH2_KEY=https://123456789-xxxx.apps.googleusercontent.com
```

---

# 30. Reiniciar o servidor

Depois de alterar variáveis no `.env`, é importante reiniciar:

```powershell
Ctrl + C
```

Depois:

```powershell
python manage.py runserver
```

porque as variáveis de ambiente são lidas quando a aplicação inicia.

---

# 31. Conferindo o Client ID carregado

Podemos abrir:

```powershell
python manage.py shell
```

e testar:

```python
from django.conf import settings

print(
    settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
)
```

Isso permite conferir se o Django está lendo o valor correto.

Nunca fazer isso com o Client Secret em uma tela compartilhada.

---

# 32. Google funcionando

Depois de corrigirmos o Client ID, o Google conseguiu:

```text
mostrar a conta
↓
autenticar
↓
retornar ao Django
```

Na URL de callback apareceram parâmetros como:

```text
state
code
scope
```

Isso confirmou que a parte do Google estava funcionando.

---

# 33. Erro `No module named 'account'`

Depois disso encontramos:

```text
ModuleNotFoundError

No module named 'account'
```

O problema não era mais Google.

Era porque copiamos o nome utilizado pelo livro:

```text
account
```

Mas nosso app é:

```text
contas
```

---

# 34. Corrigindo para `contas`

Onde estava:

```python
"account.authentication.EmailAuthBackend"
```

trocamos para:

```python
"contas.authentication.EmailAuthBackend"
```

E:

```python
"account.authentication.create_profile"
```

virou:

```python
"contas.authentication.create_profile"
```

---

# 35. Criando Profile para usuários Google

Quando alguém entra pelo Google pela primeira vez, Python Social Auth pode criar automaticamente:

```text
User
```

Mas nosso projeto possui também:

```text
Profile
```

Então adicionamos uma etapa própria na pipeline.

---

# 36. O que é a pipeline?

A pipeline é uma sequência de funções executadas durante o login social.

Mentalmente:

```text
Google retorna dados
↓
pega detalhes
↓
identifica usuário
↓
procura associação
↓
cria User se necessário
↓
cria Profile
↓
associa conta Google
↓
finaliza login
```

É como uma:

```text
linha de produção
```

---

# 37. Configuração da pipeline

No `settings.py`:

```python
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",

    "contas.authentication.create_profile",

    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]
```

---

# 38. Nossa função personalizada

No:

```text
contas/authentication.py
```

adicionamos:

```python
from .models import Profile


def create_profile(backend, user, *args, **kwargs):
    Profile.objects.get_or_create(
        user=user
    )
```

---

# 39. Para que serve?

Sempre que a pipeline passar por essa função:

```text
já existe Profile?
```

Se sim:

```text
usa o existente
```

Se não:

```text
cria
```

---

# 40. `get_or_create()`

```python
Profile.objects.get_or_create(
    user=user
)
```

significa:

```text
GET
→ procure
```

ou:

```text
CREATE
→ crie
```

---

# 41. Por que colocar depois de `create_user`?

Na pipeline:

```python
"social_core.pipeline.user.create_user",
"contas.authentication.create_profile",
```

Primeiro precisamos ter:

```text
User
```

Depois conseguimos criar:

```text
Profile
```

Fluxo:

```text
create_user
↓
User existe
↓
create_profile
↓
Profile ligado ao User
```

---

# 42. Primeiro login com Google

Uma dúvida importante foi:

```text
"Eu fiz login, mas não deveria criar conta?"
```

No login social, a primeira autenticação pode funcionar como:

```text
cadastro + login
```

ao mesmo tempo.

---

# 43. Primeira vez

```text
Usuário entra com Google
↓
Python Social Auth procura associação
↓
não encontra
↓
cria User
↓
cria Profile
↓
associa conta Google
↓
faz login
```

---

# 44. Próximas vezes

```text
Usuário entra com Google
↓
associação já existe
↓
usa o mesmo User
↓
não cria outro
↓
faz login
```

---

# 45. Verificando no Admin

No Admin confirmamos três partes.

## Usuários

```text
AUTENTICAÇÃO E AUTORIZAÇÃO
→ Usuários
```

Ali encontramos o:

```text
User
```

criado pelo login Google.

---

## Profiles

```text
CONTAS
→ Profiles
```

Ali encontramos o:

```text
Profile
```

associado ao User.

---

## User social auths

```text
PYTHON SOCIAL AUTH
→ User social auths
```

Ali encontramos a associação entre:

```text
Conta Google
↕
User Django
```

---

# 46. Estrutura final

```text
Conta Google
      │
      ▼
Python Social Auth
      │
      ▼
User Django
      │
      ▼
Profile
```

---

# 47. `runserver_plus --cert-file`

O livro utiliza:

```powershell
python manage.py runserver_plus --cert-file cinepost.crt
```

Esse comando serve para executar o servidor de desenvolvimento com:

```text
HTTPS local
```

Em vez de:

```text
http://localhost:8000
```

ele pode usar:

```text
https://localhost:8000
```

---

# 48. O que é `runserver_plus`?

É um comando fornecido pelo:

```text
django-extensions
```

Ele oferece recursos extras para desenvolvimento.

Não é o servidor de produção do Django.

---

# 49. O que faz `--cert-file`?

```text
--cert-file cinepost.crt
```

indica um certificado usado para criar:

```text
HTTPS
```

no ambiente local.

---

# 50. Precisamos dele?

No nosso caso:

```text
não
```

porque configuramos o Google para desenvolvimento com:

```text
http://localhost:8000
```

Então continuamos usando:

```powershell
python manage.py runserver
```

---

# 51. Resumo

```text
runserver
→ desenvolvimento local com HTTP
```

```text
runserver_plus
→ servidor de desenvolvimento com recursos extras
```

```text
--cert-file
→ permite HTTPS local
```

---

# 52. Produção

Quando o CinePost estiver online, NÃO utilizaremos:

```powershell
python manage.py runserver
```

nem:

```powershell
python manage.py runserver_plus
```

como servidor público de produção.

---

# 53. Desenvolvimento x produção

## Desenvolvimento

```text
Notebook
↓
Django
↓
runserver
↓
http://localhost:8000
```

---

## Produção

```text
Internet
↓
https://cinepost.com.br
↓
servidor/hospedagem
↓
servidor de aplicação Python
↓
Django
↓
PostgreSQL
```

---

# 54. Google OAuth em produção

Hoje temos:

```text
http://localhost:8000
```

e:

```text
http://localhost:8000/social-auth/complete/google-oauth2/
```

Quando o site estiver online poderemos ter:

```text
https://cinepost.com.br
```

e:

```text
https://cinepost.com.br/social-auth/complete/google-oauth2/
```

Essas URLs precisam ser adicionadas no cliente OAuth do Google.

---

# 55. O código muda muito?

Não.

A lógica permanece praticamente a mesma.

Mudam principalmente:

```text
domínio
HTTPS
variáveis de ambiente
configurações de produção
```

---

# 56. HTTPS em produção

Em produção geralmente utilizamos:

```text
certificado SSL/TLS real
```

A hospedagem frequentemente consegue gerar e renovar isso automaticamente.

Não usamos simplesmente o:

```text
cinepost.crt
```

do ambiente de desenvolvimento como certificado público.

---

# 57. Google Login é pago?

O login OAuth básico com Google não significa que cada login terá uma cobrança.

O que pode gerar custos em um site real é principalmente:

```text
hospedagem
servidor
PostgreSQL
armazenamento
domínio
```

---

# 58. Outras configurações de produção

Hoje provavelmente utilizamos:

```python
DEBUG = True
```

Em produção:

```python
DEBUG = False
```

Também configuraremos coisas como:

```python
ALLOWED_HOSTS = [
    "cinepost.com.br",
    "www.cinepost.com.br",
]
```

E possivelmente:

```python
CSRF_TRUSTED_ORIGINS = [
    "https://cinepost.com.br",
]
```

---

# 59. Segredos continuam no ambiente

Mesmo em produção:

```text
Client Secret Google
SECRET_KEY
senha PostgreSQL
credenciais de e-mail
```

não devem ficar diretamente no código.

Continuamos trabalhando com:

```text
variáveis de ambiente
```

---

# 60. Fluxo completo final

```text
Usuário abre login
↓
clica "Entrar com Google"
↓
form POST
↓
social:begin
↓
Python Social Auth gera state
↓
Google OAuth
↓
usuário escolhe a conta
↓
Google autentica
↓
Google retorna code + state
↓
/social-auth/complete/google-oauth2/
↓
Python Social Auth executa pipeline
↓
procura usuário
↓
se não existir:
cria User
↓
create_profile()
↓
cria Profile
↓
associa Google ao User
↓
login concluído
↓
usuário entra no CinePost
```

---

# 61. Principais erros que encontramos

## `Missing needed parameter state`

Causa:

```text
callback aberto diretamente
```

Solução:

```text
iniciar sempre pelo botão Entrar com Google
```

---

## HTTP 405

Causa:

```text
social:begin chamado com GET
```

Solução:

```text
usar formulário POST + csrf_token
```

---

## `invalid_client`

Causa:

```text
Client ID incorreto
```

No nosso caso havia:

```text
https://
```

no início do Client ID.

Solução:

```text
usar Client ID puro
```

---

## `No module named 'account'`

Causa:

```text
nome do app copiado do livro
```

Livro:

```text
account
```

Nosso projeto:

```text
contas
```

Solução:

```python
"contas.authentication..."
```

---

# 62. Arquivos principais envolvidos

## `.env`

Contém:

```env
CINEPOST_GOOGLE_OAUTH2_KEY=...
CINEPOST_GOOGLE_OAUTH2_SECRET=...
```

---

## `config/settings.py`

Contém:

```text
social_django
AUTHENTICATION_BACKENDS
credenciais Google
SOCIAL_AUTH_PIPELINE
```

---

## `config/urls.py`

Contém:

```python
path(
    "social-auth/",
    include(
        "social_django.urls",
        namespace="social",
    ),
)
```

---

## `contas/authentication.py`

Contém:

```python
EmailAuthBackend
```

e:

```python
create_profile()
```

---

## `login.html`

Contém o formulário:

```django
<form
    method="post"
    action="{% url 'social:begin' 'google-oauth2' %}"
>
    {% csrf_token %}

    <button type="submit">
        Entrar com Google
    </button>
</form>
```

---

# 63. Resumo mental

```text
OAuth 2.0
= autenticação/autorização usando provedor externo
```

```text
GoogleOAuth2
= backend responsável pelo Google
```

```text
Client ID
= identificação da aplicação
```

```text
Client Secret
= segredo da aplicação
```

```text
Redirect URI
= endereço para onde Google retorna
```

```text
social_django
= integração entre Django e Python Social Auth
```

```text
social:begin
= inicia autenticação social
```

```text
complete/google-oauth2
= recebe o retorno do Google
```

```text
state
= parâmetro de segurança do fluxo OAuth
```

```text
pipeline
= sequência de etapas executadas no login social
```

```text
create_profile
= nossa etapa personalizada
```

```text
get_or_create
= busca Profile existente ou cria um novo
```

---

# Principal aprendizado

O login com Google não significa simplesmente colocar um botão na página.

Existe um fluxo completo:

```text
Django
↓
Python Social Auth
↓
Google OAuth
↓
Google
↓
callback
↓
pipeline
↓
User
↓
Profile
```

A primeira autenticação pode funcionar como:

```text
cadastro + login
```

e as próximas autenticações reutilizam o usuário que já está associado àquela conta Google.

Com isso, o CinePost passou a suportar autenticação social através do Google OAuth 2.0.