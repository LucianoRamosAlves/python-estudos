# ============================================================
# ARQUIVO 2 — 02_guia_templates_autenticacao_django.md
# ============================================================

# Django — Guia dos Templates de Autenticação

## Por que existem tantos arquivos HTML?

A pasta:

```text
registration/
```

começou a ficar grande porque cada etapa da autenticação possui uma tela diferente.

Pense primeiro nas funcionalidades:

```text
Login
Logout

Troca de senha

Esqueci minha senha
```

Cada uma precisa de uma ou mais telas.

---

# Estrutura atual

Temos aproximadamente:

```text
contas/
└── templates/
    ├── contas/
    │   └── login.html
    │
    └── registration/
        ├── login.html
        ├── logged_out.html
        ├── password_change_form.html
        ├── password_change_done.html
        ├── password_reset_form.html
        ├── password_reset_email.html
        ├── password_reset_done.html
        ├── password_reset_confirm.html
        └── password_reset_complete.html
```

Agora vamos entender cada um.

---

# 1. contas/login.html

Esse arquivo pertence ao:

```text
login manual antigo
```

Nós o criamos quando tínhamos nossa própria:

```python
user_login()
```

e nosso próprio:

```python
LoginForm
```

O fluxo era:

```text
user_login()
↓
contas/login.html
```

Depois substituímos esse sistema pela `LoginView` pronta do Django.

Por isso esse arquivo normalmente não é mais utilizado.

Ele pode ser mantido como material de estudo ou removido futuramente.

---

# 2. registration/login.html

Esse é o login utilizado pela:

```python
LoginView
```

Fluxo:

```text
usuário acessa login
↓
LoginView
↓
registration/login.html
```

Esse arquivo mostra:

```text
usuário
senha
botão Entrar
erros
link "Esqueci minha senha"
```

---

## Destaques importantes

Dentro dele podemos encontrar:

```django
form.errors
```

Usamos isso para saber se houve erro na autenticação.

Também temos:

```text
next
```

que pode guardar a página para onde o usuário deve voltar depois do login.

E temos:

```django
{% csrf_token %}
```

porque o formulário de login utiliza POST.

---

# 3. registration/logged_out.html

Esse arquivo representa:

```text
logout concluído
```

Ele pode ser utilizado pela:

```python
LogoutView
```

Fluxo:

```text
usuário
↓
Sair
↓
LogoutView
↓
logged_out.html
```

Normalmente mostra algo como:

```text
Você saiu da sua conta.

Entrar novamente.
```

---

# 4. password_change_form.html

Esse arquivo é usado quando o usuário quer:

```text
trocar sua senha
```

Importante:

```text
ele já está logado
e conhece a senha atual
```

Fluxo:

```text
PasswordChangeView
↓
password_change_form.html
```

A página normalmente pede:

```text
Senha atual
Nova senha
Repita a nova senha
```

---

# 5. password_change_done.html

Esse é o segundo e último arquivo do processo de troca de senha.

Ele aparece quando a alteração foi concluída.

Fluxo:

```text
password_change_form.html
↓
senha alterada
↓
PasswordChangeDoneView
↓
password_change_done.html
```

Normalmente mostra:

```text
Sua senha foi alterada com sucesso.
```

---

# Troca de senha — mapa rápido

```text
password_change_form.html
↓
password_change_done.html
```

Só existem duas etapas principais.

---

# 6. password_reset_form.html

Agora começamos o processo:

```text
Esqueci minha senha
```

Esse arquivo mostra o formulário onde o usuário informa:

```text
e-mail
```

Fluxo:

```text
Esqueci minha senha
↓
PasswordResetView
↓
password_reset_form.html
```

Esse é o começo da recuperação.

---

# 7. password_reset_email.html

Esse arquivo é diferente de quase todos os outros.

Ele NÃO representa uma página comum do site.

Ele representa:

```text
o conteúdo do e-mail
```

O Django utiliza esse arquivo para montar o e-mail de recuperação.

Fluxo:

```text
usuário informa e-mail
↓
PasswordResetView
↓
gera UID + token
↓
password_reset_email.html
↓
Django monta mensagem
↓
envia e-mail
```

---

## Variáveis importantes

Esse template pode receber informações como:

```text
email
protocol
domain
uid
token
user
```

---

## protocol

Representa:

```text
http
```

ou:

```text
https
```

---

## domain

Representa o domínio do site.

No nosso ambiente de desenvolvimento:

```text
localhost:8000
```

Precisamos corrigir isso durante nossos testes porque estava com a porta errada.

---

## uid

É uma identificação codificada do usuário.

Ajuda o Django a saber:

```text
qual usuário quer redefinir a senha
```

---

## token

É o código temporário de segurança.

Ele permite verificar se o link é válido.

---

# 8. password_reset_done.html

Esse arquivo aparece depois que o usuário envia o formulário com o e-mail.

Fluxo:

```text
password_reset_form.html
↓
envia e-mail
↓
PasswordResetView
↓
password_reset_done.html
```

Normalmente informa:

```text
As instruções de recuperação foram enviadas.
```

---

## Muito importante

Essa página NÃO significa:

```text
senha alterada
```

Ela significa:

```text
o processo de recuperação foi iniciado
```

O usuário ainda precisa acessar o e-mail.

---

# 9. password_reset_confirm.html

Esse arquivo é exibido quando o usuário abre o link recebido no e-mail.

Fluxo:

```text
e-mail
↓
link
↓
UID + token
↓
PasswordResetConfirmView
↓
password_reset_confirm.html
```

É nessa página que o usuário digita:

```text
nova senha
nova senha novamente
```

---

## validlink

Dentro desse template existe uma variável muito importante:

```text
validlink
```

Ela é fornecida pela:

```python
PasswordResetConfirmView
```

Se:

```text
validlink = True
```

o formulário para criar a nova senha é exibido.

Se:

```text
validlink = False
```

o sistema mostra que o link não é válido.

---

## Por que um link pode ser inválido?

Por exemplo:

```text
token incorreto
token expirado
link já utilizado
dados incompatíveis
```

---

# 10. password_reset_complete.html

Esse é o último HTML da recuperação.

Ele aparece quando a nova senha foi salva.

Fluxo:

```text
password_reset_confirm.html
↓
nova senha
↓
Django salva
↓
PasswordResetCompleteView
↓
password_reset_complete.html
```

Normalmente mostra:

```text
Senha redefinida.

Agora você pode entrar novamente.
```

---

# Fluxo completo do password reset

Agora os cinco arquivos ficam mais fáceis de entender:

```text
password_reset_form.html
↓
usuário informa e-mail

password_reset_email.html
↓
Django envia o link

password_reset_done.html
↓
avisa que as instruções foram enviadas

password_reset_confirm.html
↓
usuário abre o link e cria nova senha

password_reset_complete.html
↓
processo finalizado
```

---

# Troca de senha x recuperação de senha

Essa distinção é fundamental.

## Password Change

Significa:

```text
Eu sei minha senha
mas quero trocá-la.
```

Arquivos:

```text
password_change_form.html
↓
password_change_done.html
```

---

## Password Reset

Significa:

```text
Esqueci minha senha
e preciso recuperar minha conta.
```

Arquivos:

```text
password_reset_form.html
↓
password_reset_email.html
↓
password_reset_done.html
↓
password_reset_confirm.html
↓
password_reset_complete.html
```

---

# Analogia do fluxo de recuperação

Imagine cinco etapas.

## Etapa 1

```text
password_reset_form.html
```

Pergunta:

```text
Qual é o seu e-mail?
```

---

## Etapa 2

```text
password_reset_email.html
```

Diz:

```text
Aqui está seu link de recuperação.
```

---

## Etapa 3

```text
password_reset_done.html
```

Diz:

```text
Enviamos as instruções.
Confira seu e-mail.
```

---

## Etapa 4

```text
password_reset_confirm.html
```

Pergunta:

```text
Seu link é válido?

Se sim:
qual será sua nova senha?
```

---

## Etapa 5

```text
password_reset_complete.html
```

Diz:

```text
Pronto.
Sua nova senha foi salva.
```

---

# Os dois login.html

Essa é outra coisa que pode causar confusão.

Temos:

```text
contas/login.html
```

e:

```text
registration/login.html
```

Eles não possuem a mesma função no nosso histórico.

---

## contas/login.html

Foi criado para:

```text
login manual
```

Usado pela nossa antiga:

```python
user_login()
```

---

## registration/login.html

É usado pela:

```python
LoginView
```

Esse é o login atual quando utilizamos o sistema pronto do Django.

Então mentalmente:

```text
contas/login.html
= exercício antigo
```

```text
registration/login.html
= login atual
```

---

# Por que a pasta se chama registration?

O nome:

```text
registration
```

pode enganar.

Você pode pensar:

```text
"Então aqui só fica cadastro?"
```

Não.

Esse é simplesmente o caminho padrão utilizado por várias views de autenticação do Django.

Por isso nela encontramos:

```text
login
logout
troca de senha
recuperação de senha
```

---

# Mapa final dos arquivos

| Arquivo | Serve para |
|---|---|
| `contas/login.html` | Login manual antigo |
| `registration/login.html` | Login atual da LoginView |
| `registration/logged_out.html` | Página após logout |
| `registration/password_change_form.html` | Formulário para trocar a senha |
| `registration/password_change_done.html` | Confirmação da troca de senha |
| `registration/password_reset_form.html` | Início do "Esqueci minha senha" |
| `registration/password_reset_email.html` | Conteúdo do e-mail com o link |
| `registration/password_reset_done.html` | Informa que as instruções foram enviadas |
| `registration/password_reset_confirm.html` | Página para criar nova senha |
| `registration/password_reset_complete.html` | Recuperação concluída |

---

# Resumo mais curto possível

```text
login.html
= entrar
```

```text
logged_out.html
= saiu
```

```text
password_change_form.html
= trocar senha
```

```text
password_change_done.html
= senha trocada
```

```text
password_reset_form.html
= informar e-mail
```

```text
password_reset_email.html
= e-mail com link
```

```text
password_reset_done.html
= e-mail solicitado
```

```text
password_reset_confirm.html
= criar nova senha
```

```text
password_reset_complete.html
= recuperação terminou
```

---

# Forma mais fácil de decorar

Não tente decorar os nomes dos nove arquivos.

Decore primeiro apenas isto:

```text
LOGIN
↓
login.html
```

```text
LOGOUT
↓
logged_out.html
```

```text
TROCAR SENHA
↓
form
↓
done
```

```text
ESQUECI A SENHA
↓
form
↓
email
↓
done
↓
confirm
↓
complete
```

Depois os nomes dos arquivos começam a ficar naturais.