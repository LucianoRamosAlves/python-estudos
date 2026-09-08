# ARQUIVO 1 — 01_resumo_autenticacao_django_ate_aqui.md

# Django — Resumo da Autenticação até Aqui

## Objetivo desta etapa

Nesta parte do CinePost, começamos a usar o sistema de autenticação que já vem com o Django.

O caminho de aprendizado foi:

```text
Entender o sistema de autenticação
↓
Criar login manual
↓
Substituir pelo LoginView do Django
↓
Adicionar logout
↓
Adicionar troca de senha
↓
Adicionar recuperação de senha
↓
Simplificar as URLs usando django.contrib.auth.urls
```

---

# 1. O sistema de autenticação do Django

O Django já possui um sistema pronto localizado em:

```python
django.contrib.auth
```

Ele fornece recursos para:

- usuários;
- login;
- logout;
- sessões;
- grupos;
- permissões;
- troca de senha;
- recuperação de senha.

Isso significa que não precisamos construir toda a autenticação do zero.

---

# 2. User, Group e Permission

O Django já possui alguns Models relacionados à autenticação.

## User

Representa uma conta de usuário.

Algumas informações importantes são:

```text
username
password
email
first_name
last_name
is_active
```

Também existem campos como:

```text
is_staff
is_superuser
```

---

## Group

Permite agrupar usuários.

Exemplo:

```text
Editores
Moderadores
Administradores
```

---

## Permission

Representa permissões para determinadas ações.

Exemplo:

```text
pode adicionar
pode alterar
pode excluir
pode visualizar
```

---

# 3. Sessões e Middleware

Dois middlewares são muito importantes para autenticação.

## SessionMiddleware

Mantém a sessão do usuário entre as requisições.

```text
login
↓
sessão criada
↓
abre outra página
↓
continua logado
```

---

## AuthenticationMiddleware

Associa o usuário da sessão à requisição atual.

Por isso conseguimos utilizar:

```python
request.user
```

---

# 4. Login manual

Primeiro criamos um login manual para entender como o processo funciona.

O fluxo era:

```text
formulário
↓
username + password
↓
POST
↓
form.is_valid()
↓
authenticate()
↓
verifica is_active
↓
login()
↓
sessão
```

---

# 5. authenticate()

O:

```python
authenticate()
```

confere as credenciais.

Ele verifica:

```text
usuário existe?
↓
senha está correta?
```

Se estiver tudo certo:

```text
retorna um objeto User
```

Se estiver errado:

```python
None
```

---

# 6. login()

Depois de autenticar o usuário usamos:

```python
login(request, user)
```

O `login()` coloca o usuário na sessão.

A diferença principal é:

```text
authenticate()
= verificar a identidade
```

```text
login()
= iniciar a sessão autenticada
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
sessão
```

---

# 7. LoginForm manual

Também criamos nosso próprio:

```python
LoginForm
```

Ele recebia:

```text
username
password
```

Esse formulário foi criado para entendermos o funcionamento do login.

Depois que passamos a usar o sistema pronto do Django, ele deixou de ser necessário para o login padrão.

---

# 8. LoginView pronta do Django

Depois substituímos nossa view manual pela:

```python
LoginView
```

Agora o Django realiza grande parte do processo.

Fluxo:

```text
LoginView
↓
AuthenticationForm
↓
validação
↓
autenticação
↓
sessão
```

---

# 9. AuthenticationForm

A `LoginView` utiliza automaticamente:

```python
AuthenticationForm
```

Esse formulário já trabalha com:

```text
username
password
validação
autenticação
erros
```

Por isso não precisamos criar novamente toda a lógica do login.

---

# 10. form.errors

No template podemos verificar:

```django
{% if form.errors %}
```

Isso permite mostrar uma mensagem quando:

```text
usuário ou senha estão incorretos
```

---

# 11. O parâmetro next

Também aprendemos sobre:

```text
next
```

Ele guarda a página que o usuário queria acessar antes de ir para o login.

Exemplo:

```text
usuário tenta acessar página protegida
↓
não está autenticado
↓
vai para login
↓
faz login
↓
volta para página original
```

No formulário podemos manter esse valor com um campo escondido.

---

# 12. LogoutView

Para logout utilizamos:

```python
LogoutView
```

Ela encerra a sessão do usuário.

No Django atual o logout é feito através de:

```text
POST
```

Fluxo:

```text
usuário logado
↓
botão Sair
↓
POST
↓
LogoutView
↓
sessão encerrada
```

---

# 13. Troca de senha

Depois adicionamos:

```python
PasswordChangeView
```

e:

```python
PasswordChangeDoneView
```

Essa funcionalidade é usada quando:

```text
usuário está logado
+
sabe a senha atual
+
quer trocar por outra
```

Fluxo:

```text
PasswordChangeView
↓
senha atual
↓
nova senha
↓
confirmação
↓
Django valida
↓
senha alterada
↓
PasswordChangeDoneView
```

---

# 14. Recuperação de senha

Depois implementamos:

```text
Esqueci minha senha
```

Esse processo é diferente da troca de senha.

Aqui o usuário pode não conseguir acessar a conta porque esqueceu sua senha.

O Django fornece:

```text
PasswordResetView
PasswordResetDoneView
PasswordResetConfirmView
PasswordResetCompleteView
```

---

# 15. PasswordResetView

É o início do processo.

O usuário informa:

```text
e-mail
```

O Django procura a conta correspondente e prepara o processo de recuperação.

---

# 16. PasswordResetDoneView

Depois da solicitação, essa view mostra uma página informando que as instruções de recuperação foram enviadas.

Importante:

```text
isso ainda não significa que a senha foi alterada
```

O usuário ainda precisa abrir o link.

---

# 17. PasswordResetConfirmView

Essa view recebe o link enviado por e-mail.

Ela verifica:

```text
UID
+
token
```

Se estiver tudo válido, permite que o usuário crie uma nova senha.

---

# 18. PasswordResetCompleteView

Depois que a nova senha é salva, essa view mostra a página final.

Fluxo:

```text
nova senha criada
↓
PasswordResetCompleteView
↓
recuperação concluída
```

---

# 19. Fluxo completo da recuperação

```text
Usuário informa o e-mail
↓
PasswordResetView
↓
Django gera UID + token
↓
e-mail é enviado
↓
usuário abre o link
↓
PasswordResetConfirmView
↓
token é verificado
↓
usuário cria nova senha
↓
Django salva a senha
↓
PasswordResetCompleteView
```

---

# 20. UID

O link contém uma identificação do usuário.

No código aparece como:

```text
uidb64
```

Ele permite ao Django saber qual conta está sendo recuperada.

---

# 21. Token

O Django também gera um:

```text
token
```

Esse token funciona como uma autorização temporária.

Ele não é a senha.

Ele serve para validar o pedido de redefinição.

---

# 22. validlink

Dentro do template:

```text
password_reset_confirm.html
```

podemos usar:

```django
{% if validlink %}
```

A `PasswordResetConfirmView` informa se o link pode ser utilizado.

Se:

```text
validlink = True
```

mostramos o formulário da nova senha.

Se:

```text
validlink = False
```

mostramos que o link é inválido ou não pode mais ser usado.

---

# 23. A senha antiga não é recuperada

O Django não envia a senha antiga por e-mail.

A senha não é armazenada no banco como texto normal.

Ela é armazenada utilizando:

```text
hash
```

Por isso o processo é:

```text
esqueceu a senha
↓
não recuperamos a senha antiga
↓
criamos uma nova senha
```

---

# 24. Link de recuperação

Durante nosso teste, o Django enviou um link de recuperação por e-mail.

Inicialmente o domínio estava com uma porta incorreta.

Estava semelhante a:

```text
localhost:80000
```

e corrigimos para:

```text
localhost:8000
```

Depois disso o link funcionou.

---

# 25. Teste realizado

O fluxo completo funcionou:

```text
solicitar recuperação
↓
receber e-mail
↓
abrir link
↓
token válido
↓
criar nova senha
↓
salvar
↓
entrar novamente
```

---

# 26. URLs escritas manualmente

Durante o aprendizado escrevemos manualmente URLs para:

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

Isso foi útil para entender qual URL chama qual view.

---

# 27. django.contrib.auth.urls

Depois o livro mostra que o Django já possui um conjunto dessas URLs pronto.

Podemos utilizar:

```python
include("django.contrib.auth.urls")
```

Essa linha inclui as URLs padrão relacionadas a:

```text
login
logout
troca de senha
recuperação de senha
```

---

# 28. Por que fizemos manualmente primeiro?

Porque agora sabemos o que existe dentro desse atalho.

A ordem foi:

```text
escrever manualmente
↓
entender cada view
↓
testar
↓
usar include()
```

Então:

```python
include("django.contrib.auth.urls")
```

não é mágica.

Ele simplesmente inclui várias URLs que o Django já definiu.

---

# 29. Templates continuam personalizados

Mesmo usando:

```python
django.contrib.auth.urls
```

os HTMLs continuam podendo ser nossos.

A divisão fica:

```text
Django
→ lógica de autenticação
```

```text
CinePost
→ templates e aparência
```

---

# 30. A pasta registration

As views prontas do sistema de autenticação procuram vários templates dentro de:

```text
templates/registration/
```

Por isso criamos vários arquivos nessa pasta.

Cada arquivo representa uma etapa específica.

---

# Estado atual

Até aqui aprendemos:

```text
✅ django.contrib.auth
✅ User
✅ Group
✅ Permission
✅ SessionMiddleware
✅ AuthenticationMiddleware
✅ request.user
✅ login manual
✅ LoginForm
✅ authenticate()
✅ login()
✅ is_active
✅ LoginView
✅ AuthenticationForm
✅ LogoutView
✅ next
✅ PasswordChangeView
✅ PasswordChangeDoneView
✅ PasswordResetView
✅ PasswordResetDoneView
✅ PasswordResetConfirmView
✅ PasswordResetCompleteView
✅ UID
✅ token
✅ validlink
✅ recuperação por e-mail
✅ django.contrib.auth.urls
```

---

# Resumo mental

## Login

```text
usuário + senha
↓
LoginView
↓
AuthenticationForm
↓
sessão
```

## Logout

```text
POST
↓
LogoutView
↓
sessão encerrada
```

## Troca de senha

```text
usuário logado
↓
PasswordChangeView
↓
senha atual
↓
nova senha
↓
PasswordChangeDoneView
```

## Recuperação de senha

```text
e-mail
↓
PasswordResetView
↓
UID + token
↓
link
↓
PasswordResetConfirmView
↓
nova senha
↓
PasswordResetCompleteView
```

---

# Próxima etapa

O próximo assunto é:

```text
Cadastro de usuários
```

Depois disso começaremos a trabalhar com:

```text
perfil de usuário
```
