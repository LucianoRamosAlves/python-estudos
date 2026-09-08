# Django — Resumo Completo de Registro, Perfil e Custom User

## Visão geral

Nesta parte do CinePost, saímos de um sistema em que os usuários apenas conseguiam:

```text
login
logout
trocar senha
recuperar senha
```

e passamos a permitir também:

```text
criar conta
↓
criar Profile
↓
editar dados do User
↓
editar dados do Profile
↓
enviar foto de perfil
```

A estrutura atual ficou conceitualmente assim:

```text
User
↕
1 para 1
↕
Profile
```

O `User` continua sendo o usuário padrão do Django.

O `Profile` guarda informações extras.

---

# 1. Registro de usuários

Até então, os usuários precisavam existir previamente no banco.

Criamos um sistema para permitir que visitantes criem sua própria conta.

Fluxo:

```text
Visitante
↓
/contas/register/
↓
preenche formulário
↓
Django valida
↓
cria User
↓
trata senha
↓
salva User
↓
cria Profile
↓
usuário pode fazer login
```

---

# 2. UserRegistrationForm

Criamos:

```python
UserRegistrationForm
```

utilizando:

```python
forms.ModelForm
```

Isso acontece porque o formulário realmente cria um objeto no banco.

---

# 3. Form x ModelForm

## Login

No login usamos:

```python
forms.Form
```

porque apenas recebemos:

```text
username
password
```

para verificar uma conta existente.

---

## Cadastro

No cadastro usamos:

```python
forms.ModelForm
```

porque queremos:

```text
criar um novo User
```

Mentalmente:

```text
Form
→ recebe/processa dados
```

```text
ModelForm
→ recebe dados ligados a um Model
```

---

# 4. get_user_model()

No formulário usamos:

```python
get_user_model()
```

Isso significa:

```text
Django, me dê o Model de usuário configurado neste projeto.
```

É melhor do que importar diretamente:

```python
User
```

porque o projeto poderia utilizar um Model de usuário personalizado no futuro.

---

# 5. Campos do cadastro

O formulário utiliza campos do User:

```text
username
first_name
email
```

E criamos também:

```text
password
password2
```

---

# 6. password2

O campo:

```text
password2
```

não existe no Model `User`.

Ele existe apenas no formulário para confirmar a senha.

Exemplo:

```text
Senha:
123456

Repita a senha:
123456
```

---

# 7. clean_password2()

Criamos:

```python
clean_password2()
```

Esse método é executado durante:

```python
form.is_valid()
```

Ele compara:

```text
password
password2
```

Se forem diferentes:

```text
ValidationError
```

Se forem iguais:

```text
formulário continua válido
```

---

# 8. clean_<campo>()

O Django possui o padrão:

```python
clean_nome_do_campo()
```

Exemplos:

```python
clean_email()
clean_username()
clean_password2()
```

Serve para adicionar validações específicas a um campo.

---

# 9. clean()

Também existe:

```python
clean()
```

que pode validar o formulário como um todo.

Nesta situação utilizamos:

```python
clean_password2()
```

porque estamos validando especificamente a confirmação da senha.

---

# 10. Username único

Não precisamos consultar manualmente se o username já existe.

O campo `username` do User já possui uma restrição de unicidade.

Então o próprio ModelForm consegue detectar:

```text
username repetido
↓
erro de validação
```

---

# 11. View register

Criamos:

```python
register()
```

Ela trabalha com:

```text
GET
POST
```

---

# 12. GET no register

Quando acessamos:

```text
/contas/register/
```

temos:

```text
GET
↓
UserRegistrationForm vazio
↓
register.html
```

---

# 13. POST no register

Depois que o usuário envia:

```text
POST
↓
UserRegistrationForm(request.POST)
↓
is_valid()
```

Se estiver válido:

```text
criamos o usuário
```

---

# 14. save(commit=False)

Utilizamos:

```python
new_user = user_form.save(commit=False)
```

Isso significa:

```text
crie o objeto User
mas ainda não salve no banco
```

Mentalmente:

```text
form
↓
User em memória
↓
ainda não salvo
```

---

# 15. Por que commit=False?

Porque precisamos tratar a senha antes de salvar.

Fluxo:

```text
criar User
↓
não salvar ainda
↓
tratar senha
↓
salvar
```

---

# 16. set_password()

Depois usamos:

```python
new_user.set_password(...)
```

Isso é extremamente importante.

Não devemos fazer:

```python
new_user.password = "123456"
```

A senha precisa passar pelo sistema de hashing do Django.

---

# 17. Hash de senha

O banco não deve guardar:

```text
123456
```

Ele guarda uma representação hash.

Fluxo:

```text
senha digitada
↓
set_password()
↓
hash
↓
banco
```

---

# 18. O Django não conhece a senha original

Por isso o Django não consegue simplesmente mostrar uma senha esquecida.

O sistema funciona através de:

```text
verificação de hash
```

Então:

```text
esqueci minha senha
↓
crio uma nova
```

em vez de:

```text
Django mostra a senha antiga
```

---

# 19. PASSWORD_HASHERS

O Django possui:

```python
PASSWORD_HASHERS
```

que define os algoritmos utilizados para senhas.

O livro cita algoritmos como:

```text
PBKDF2
PBKDF2SHA1
Argon2
BCrypt
Scrypt
```

O importante é:

```text
não implementamos hashing manualmente
```

O Django cuida disso.

---

# 20. Salvando o User

Depois:

```python
new_user.save()
```

Agora o usuário é salvo no banco.

Fluxo:

```text
save(commit=False)
↓
set_password()
↓
save()
```

---

# 21. register.html

Criamos:

```text
contas/templates/contas/register.html
```

Esse template mostra:

```text
username
nome
e-mail
senha
confirmação da senha
```

e envia via:

```text
POST
```

com:

```django
{% csrf_token %}
```

---

# 22. register_done.html

Criamos:

```text
contas/templates/contas/register_done.html
```

Essa página aparece depois que a conta é criada.

Ela recebe:

```text
new_user
```

Então podemos mostrar:

```django
{{ new_user.first_name }}
```

---

# 23. URL de registro

Criamos:

```text
/contas/register/
```

com nome:

```text
register
```

Então podemos usar:

```django
{% url "register" %}
```

---

# 24. Link de cadastro no login

No:

```text
registration/login.html
```

adicionamos um link:

```text
Ainda não possui conta?
Cadastre-se
```

Fluxo:

```text
login
↓
cadastre-se
↓
/contas/register/
```

---

# 25. User x Profile

Depois começamos a trabalhar com dados extras.

O User padrão já possui:

```text
username
password
email
first_name
last_name
```

Mas queríamos adicionar:

```text
data de nascimento
foto
```

Então criamos:

```python
Profile
```

---

# 26. Model Profile

O Profile contém:

```text
user
date_of_birth
photo
```

---

# 27. OneToOneField

O relacionamento entre User e Profile é:

```python
OneToOneField
```

Isso significa:

```text
1 User
↕
1 Profile
```

Não podemos ter:

```text
1 User
↓
vários Profiles
```

---

# 28. ForeignKey x OneToOneField

## ForeignKey

Permite:

```text
muitos objetos
↓
um objeto
```

Exemplo:

```text
vários posts
↓
um autor
```

---

## OneToOneField

Permite:

```text
um objeto
↔
um objeto
```

Exemplo:

```text
User Luciano
↔
Profile Luciano
```

---

# 29. settings.AUTH_USER_MODEL

No relacionamento usamos:

```python
settings.AUTH_USER_MODEL
```

Isso evita apontar diretamente para:

```python
auth.User
```

e mantém o código compatível com possíveis custom users.

---

# 30. get_user_model() x AUTH_USER_MODEL

Uma distinção importante.

## get_user_model()

Usamos quando queremos obter a classe User no código.

Exemplo conceitual:

```text
forms
views
funções
```

---

## settings.AUTH_USER_MODEL

Usamos principalmente ao declarar relacionamentos em Models.

Exemplo:

```python
ForeignKey
OneToOneField
```

---

# 31. on_delete=models.CASCADE

No Profile temos:

```python
on_delete=models.CASCADE
```

Então:

```text
User apagado
↓
Profile apagado
```

Isso evita deixar um Profile sem usuário.

---

# 32. date_of_birth

Criamos:

```python
DateField
```

com:

```text
blank=True
null=True
```

---

# 33. blank x null

## blank=True

Relacionado principalmente a:

```text
validação/formulário
```

Significa:

```text
campo pode ficar vazio
```

---

## null=True

Relacionado ao banco.

Significa:

```text
banco pode armazenar NULL
```

---

# 34. photo

Criamos:

```python
ImageField
```

para permitir foto de perfil.

O banco não guarda a imagem inteira.

Ele guarda:

```text
caminho do arquivo
```

A imagem física fica no sistema de arquivos.

---

# 35. upload_to

Utilizamos algo semelhante a:

```text
users/%Y/%m/%d/
```

Isso organiza os arquivos por data.

Exemplo:

```text
media/
└── users/
    └── 2026/
        └── 09/
            └── 08/
                └── foto.jpg
```

---

# 36. Pillow

O Django utiliza a biblioteca:

```text
Pillow
```

para trabalhar com:

```python
ImageField
```

Ela é usada para validação e processamento básico de imagens.

---

# 37. MEDIA_ROOT

Configuramos:

```python
MEDIA_ROOT
```

Ele representa:

```text
onde os arquivos enviados ficam fisicamente
```

Exemplo:

```text
projeto/media/
```

---

# 38. MEDIA_URL

Configuramos:

```python
MEDIA_URL
```

Ele representa:

```text
qual URL será usada para acessar os arquivos
```

Exemplo:

```text
/media/
```

---

# 39. MEDIA_ROOT x MEDIA_URL

Mentalmente:

```text
MEDIA_ROOT
= pasta física
```

```text
MEDIA_URL
= endereço no navegador
```

---

# 40. Static x Media

## Static

Arquivos que pertencem ao site.

Exemplos:

```text
CSS
JavaScript
logo
ícones
```

---

## Media

Arquivos enviados por usuários.

Exemplos:

```text
foto de perfil
imagem de post
arquivo enviado
```

---

# 41. Servindo media em desenvolvimento

No:

```text
config/urls.py
```

configuramos o Django para servir arquivos de media quando:

```python
DEBUG = True
```

Isso serve apenas para desenvolvimento.

Em produção, normalmente outro serviço deve servir esses arquivos.

---

# 42. Migration do Profile

Depois de criar o Model:

```python
Profile
```

executamos:

```text
makemigrations
↓
migrate
```

Fluxo:

```text
models.py
↓
makemigrations
↓
migration
↓
migrate
↓
tabela criada no PostgreSQL
```

---

# 43. Tabela Profile

Conceitualmente temos:

```text
contas_profile
-------------------
id
user_id
date_of_birth
photo
```

O:

```text
user_id
```

liga o Profile ao User.

---

# 44. Profile no Admin

Registramos:

```python
Profile
```

no Django Admin.

Agora podemos:

```text
visualizar
criar
editar
```

Profiles pelo:

```text
/admin/
```

---

# 45. ProfileAdmin

No Admin configuramos:

```text
list_display
```

para escolher as colunas exibidas.

Exemplo:

```text
user
date_of_birth
photo
```

---

# 46. raw_id_fields

Também usamos:

```python
raw_id_fields
```

para o campo:

```text
user
```

Isso altera a forma como relacionamentos são selecionados no Admin.

É útil principalmente quando existem muitos registros.

---

# 47. Usuários antigos não tinham Profile

Quando criamos a tabela Profile, os usuários que já existiam continuaram existindo sem Profile.

Então poderíamos ter:

```text
User ✅
Profile ❌
```

Por isso criamos Profiles manualmente para os usuários antigos usados nos testes.

---

# 48. Criando Profile automaticamente no registro

Depois modificamos:

```python
register()
```

Após:

```python
new_user.save()
```

adicionamos:

```python
Profile.objects.create(user=new_user)
```

Agora:

```text
novo cadastro
↓
User criado
↓
Profile criado automaticamente
```

---

# 49. Por que salvar User antes?

Porque o Profile precisa apontar para um User existente.

Então:

```text
cria User
↓
salva User
↓
User recebe ID
↓
cria Profile ligado a ele
```

---

# 50. Usuários criados no Admin

Essa criação automática acontece apenas quando usamos nossa:

```python
register()
```

Se criarmos usuário manualmente pelo Admin:

```text
Add User
```

o Profile não nasce automaticamente.

---

# 51. Signals

O livro comenta que futuramente poderíamos usar:

```text
signals
```

para criar Profile automaticamente sempre que qualquer User fosse criado.

Mas ainda não implementamos isso.

---

# 52. UserEditForm

Criamos:

```python
UserEditForm
```

para permitir editar campos do User.

Campos:

```text
first_name
last_name
email
```

---

# 53. ProfileEditForm

Criamos:

```python
ProfileEditForm
```

para editar:

```text
date_of_birth
photo
```

---

# 54. Por que dois formulários?

Porque temos dois Models:

```text
User
Profile
```

Então:

```text
UserEditForm
→ User
```

```text
ProfileEditForm
→ Profile
```

Mesmo que visualmente apareçam na mesma página.

---

# 55. View edit

Criamos:

```python
edit()
```

para editar os dois objetos juntos.

Ela é protegida com:

```python
@login_required
```

---

# 56. login_required

Isso significa:

```text
usuário autenticado
→ pode acessar
```

```text
usuário anônimo
→ não pode editar
```

---

# 57. request.user

Dentro da view usamos:

```python
request.user
```

Ele representa:

```text
o usuário atualmente autenticado
```

---

# 58. instance=request.user

No UserEditForm usamos:

```python
instance=request.user
```

Isso significa:

```text
edite este User existente
```

e não:

```text
crie um novo User
```

---

# 59. request.user.profile

Como User e Profile possuem relacionamento OneToOne, conseguimos fazer:

```python
request.user.profile
```

Isso retorna o Profile daquele usuário.

Mentalmente:

```text
request.user
↓
User
↓
.profile
↓
Profile
```

---

# 60. instance=request.user.profile

No ProfileEditForm usamos:

```python
instance=request.user.profile
```

Isso significa:

```text
edite o Profile existente desse usuário
```

---

# 61. request.POST

Os dados de texto chegam em:

```python
request.POST
```

Exemplos:

```text
nome
sobrenome
e-mail
data
```

---

# 62. request.FILES

Arquivos enviados chegam em:

```python
request.FILES
```

Exemplo:

```text
foto
```

Por isso o ProfileEditForm recebe:

```python
files=request.FILES
```

---

# 63. enctype multipart/form-data

No HTML usamos:

```html
enctype="multipart/form-data"
```

Isso é necessário para upload de arquivos.

Sem isso:

```text
campos de texto funcionam
foto não
```

---

# 64. Validando os dois formulários

Na view:

```text
UserEditForm válido?
+
ProfileEditForm válido?
```

Somente se ambos estiverem válidos:

```text
salvamos os dois
```

---

# 65. Salvando os dois Models

Chamamos:

```text
user_form.save()
profile_form.save()
```

Então:

```text
User atualizado
+
Profile atualizado
```

---

# 66. edit.html

Criamos:

```text
contas/templates/contas/edit.html
```

Essa página mostra os dois formulários.

Visualmente:

```text
Nome
Sobrenome
E-mail

Data de nascimento
Foto

[ Salvar alterações ]
```

Por baixo:

```text
UserEditForm
+
ProfileEditForm
```

---

# 67. URL edit

Criamos:

```text
/contas/edit/
```

Essa página permite editar os dados da conta e do perfil.

---

# 68. Fluxo completo da edição

```text
usuário logado
↓
/contas/edit/
↓
@login_required
↓
UserEditForm(instance=request.user)
↓
ProfileEditForm(instance=request.user.profile)
↓
edit.html
↓
usuário altera dados
↓
POST
↓
request.POST
+
request.FILES
↓
is_valid()
↓
save User
↓
save Profile
```

---

# 69. User padrão x Custom User

Depois o livro apresenta outra possibilidade.

Até agora usamos:

```text
User padrão
+
Profile
```

Mas o Django também permite substituir o User padrão por um:

```text
Custom User
```

---

# 70. AbstractUser

Um Custom User normalmente pode herdar de:

```python
AbstractUser
```

O `AbstractUser` já traz grande parte da implementação pronta:

```text
username
password
email
first_name
last_name
groups
permissions
is_active
is_staff
```

Então podemos adicionar campos extras.

---

# 71. Exemplo conceitual de Custom User

Em vez de:

```text
User
↓
Profile
```

poderíamos ter:

```text
CustomUser
├── username
├── password
├── email
├── first_name
├── last_name
├── date_of_birth
└── photo
```

---

# 72. Profile x Custom User

## Profile

Mantém:

```text
User padrão
+
Model adicional
```

Estrutura:

```text
User
↕
Profile
```

---

## Custom User

Substitui o próprio Model de usuário.

Estrutura:

```text
MeuUser
```

com os campos necessários diretamente nele.

---

# 73. Vantagem do Profile

É simples para adicionar algumas informações extras.

Exemplo:

```text
foto
data de nascimento
biografia
```

sem substituir o sistema padrão de usuário.

---

# 74. Vantagem do Custom User

Dá muito mais flexibilidade.

Exemplos:

```text
login apenas por e-mail
remover username
adicionar CPF
alterar estrutura de nomes
adicionar campos diretamente no User
```

---

# 75. Quando criar Custom User?

Idealmente:

```text
no começo do projeto
```

Trocar o User depois que o projeto já possui:

```text
migrations
dados
ForeignKeys
usuários
Profile
```

pode ser trabalhoso.

---

# 76. Por que não vamos mudar o CinePost agora?

O CinePost já possui:

```text
User padrão
Profile
PostFilme.autor
migrations
usuários
PostgreSQL com dados
```

E nossas necessidades atuais são simples:

```text
data de nascimento
foto
```

Então:

```text
User + Profile
```

continua sendo uma boa solução.

---

# 77. AbstractUser x User

Mentalmente:

```text
User
= usuário pronto do Django
```

```text
AbstractUser
= base completa para criar seu próprio User
```

---

# 78. AbstractBaseUser

Existe também:

```python
AbstractBaseUser
```

Ele é mais baixo nível.

Mentalmente:

```text
AbstractUser
→ muita coisa pronta
```

```text
AbstractBaseUser
→ exige muito mais implementação manual
```

Para muitos projetos que precisam de Custom User, `AbstractUser` é mais simples.

---

# 79. Integração com apps externos

O livro alerta que alguns pacotes podem ter problemas com custom users se forem mal implementados.

Um pacote deveria usar:

```python
get_user_model()
```

ou:

```python
settings.AUTH_USER_MODEL
```

em vez de assumir diretamente:

```python
User
```

---

# 80. Estrutura atual do CinePost

Atualmente:

```text
Django User
│
├── username
├── password
├── email
├── first_name
└── last_name
        │
        │ OneToOne
        ↓
Profile
├── date_of_birth
└── photo
```

---

# 81. Fluxo completo atual do usuário

```text
VISITANTE
↓
register
↓
UserRegistrationForm
↓
validação
↓
set_password()
↓
User salvo
↓
Profile criado
↓
login
↓
usuário autenticado
↓
edit
↓
UserEditForm
+
ProfileEditForm
↓
dados atualizados
```

---

# 82. Conceitos principais aprendidos

```text
UserRegistrationForm
= formulário de cadastro
```

```text
get_user_model()
= obtém o Model de usuário configurado
```

```text
ModelForm
= formulário ligado a um Model
```

```text
clean_password2()
= valida confirmação da senha
```

```text
commit=False
= cria objeto sem salvar imediatamente
```

```text
set_password()
= trata corretamente a senha
```

```text
Profile
= informações extras do usuário
```

```text
OneToOneField
= relação um para um
```

```text
AUTH_USER_MODEL
= referência ao Model de usuário configurado
```

```text
ImageField
= campo para imagem
```

```text
MEDIA_ROOT
= onde arquivos ficam fisicamente
```

```text
MEDIA_URL
= URL para acessar arquivos
```

```text
Pillow
= biblioteca usada para trabalhar com imagens
```

```text
UserEditForm
= edita User
```

```text
ProfileEditForm
= edita Profile
```

```text
request.user
= usuário autenticado
```

```text
request.user.profile
= Profile daquele usuário
```

```text
request.FILES
= arquivos enviados
```

```text
multipart/form-data
= necessário para upload
```

```text
Custom User
= substituição do User padrão
```

```text
AbstractUser
= base pronta para criar Custom User
```

---

# Resumo mental final

## Cadastro

```text
UserRegistrationForm
↓
clean_password2()
↓
save(commit=False)
↓
set_password()
↓
save()
↓
Profile.objects.create()
```

---

## Perfil

```text
User
1 ↔ 1
Profile
```

---

## Upload

```text
foto
↓
request.FILES
↓
ImageField
↓
MEDIA_ROOT
```

---

## Edição

```text
request.user
↓
UserEditForm

request.user.profile
↓
ProfileEditForm

↓
save()
```

---

## Custom User

```text
Opção atual:

User padrão
+
Profile
```

ou:

```text
Outra possibilidade:

Custom User
herdando AbstractUser
```

Para o CinePost atual:

```text
continuamos com User + Profile
```

porque já atende bem às necessidades e evita uma alteração estrutural grande no projeto.