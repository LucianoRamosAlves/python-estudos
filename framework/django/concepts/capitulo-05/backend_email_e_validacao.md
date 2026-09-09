# Django 5 by Example — Capítulo 5
## Backend de autenticação por e-mail e prevenção de e-mails duplicados

# Onde estamos no capítulo

Até aqui, no capítulo 5, já fizemos duas grandes melhorias no sistema de autenticação do CinePost:

```text
Django Messages ✅
Login por e-mail ✅
Prevenção de e-mails duplicados ✅
```

Agora o usuário consegue entrar usando:

```text
username + senha
```

ou:

```text
e-mail + senha
```

---

# AUTHENTICATION_BACKENDS

O Django usa backends para decidir como autenticar um usuário.

Por padrão, o backend principal é:

```python
django.contrib.auth.backends.ModelBackend
```

Ele autentica usando o sistema padrão do Django.

Mentalmente:

```text
Login
↓
authenticate()
↓
ModelBackend
↓
username + senha
```

---

# Múltiplos backends

O Django permite configurar vários backends ao mesmo tempo.

No CinePost ficou:

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "contas.authentication.EmailAuthBackend",
]
```

Então o fluxo é:

```text
authenticate()
↓
1º ModelBackend
↓
tenta username + senha
↓
falhou?
↓
2º EmailAuthBackend
↓
tenta e-mail + senha
```

Se algum backend retornar um usuário válido:

```text
autenticação concluída
```

Se todos retornarem:

```python
None
```

a autenticação falha.

---

# A ordem dos backends importa

O Django tenta os backends na ordem definida em:

```python
AUTHENTICATION_BACKENDS
```

No CinePost:

```text
1º username
2º e-mail
```

Assim mantemos o comportamento padrão e adicionamos o login por e-mail como segunda possibilidade.

---

# Arquivo authentication.py

Criamos:

```text
contas/authentication.py
```

com o backend:

```python
EmailAuthBackend
```

A ideia dele é:

```text
recebe login
↓
trata o valor como e-mail
↓
procura User
↓
verifica senha
↓
retorna User
```

---

# EmailAuthBackend

Nossa versão foi adaptada para o projeto atual:

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    Autentica usuários utilizando e-mail e senha.
    """

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        **kwargs,
    ):
        if username is None or password is None:
            return None

        User = get_user_model()

        try:
            user = User.objects.get(
                email__iexact=username
            )

        except (
            User.DoesNotExist,
            User.MultipleObjectsReturned,
        ):
            return None

        if (
            user.check_password(password)
            and self.user_can_authenticate(user)
        ):
            return user

        return None
```

---

# Por que usamos get_user_model()?

Em vez de:

```python
from django.contrib.auth.models import User
```

usamos:

```python
get_user_model()
```

Isso é melhor porque respeita o Model de usuário configurado no projeto.

Mentalmente:

```text
get_user_model()
→ me dê o User atual do projeto
```

---

# Por que herdamos de ModelBackend?

Criamos:

```python
class EmailAuthBackend(ModelBackend):
```

Assim reaproveitamos comportamentos do backend padrão.

Uma vantagem é usar:

```python
self.user_can_authenticate(user)
```

que respeita estados como:

```text
is_active = False
```

Então usuários desativados não conseguem autenticar por e-mail.

---

# Parâmetro username recebendo e-mail

Mesmo autenticando por e-mail, usamos:

```python
username
```

como parâmetro.

Isso acontece porque queremos que o backend continue compatível com o sistema padrão de login do Django.

Então:

```python
username="teste@email.com"
```

pode representar:

```text
e-mail digitado no formulário
```

---

# Busca por e-mail

Usamos:

```python
User.objects.get(
    email__iexact=username
)
```

O:

```python
iexact
```

faz comparação sem diferenciar maiúsculas de minúsculas.

Então:

```text
TESTE@EMAIL.COM
```

e:

```text
teste@email.com
```

são tratados da mesma forma na consulta.

---

# check_password()

Depois usamos:

```python
user.check_password(password)
```

Esse método verifica a senha informada contra o hash armazenado.

Nunca fazemos:

```python
user.password == password
```

porque a senha não fica salva em texto puro.

Fluxo:

```text
senha digitada
↓
check_password()
↓
comparação segura com hash
↓
True ou False
```

---

# user_can_authenticate()

Depois verificamos:

```python
self.user_can_authenticate(user)
```

Isso impede autenticação de usuários que não podem autenticar.

Exemplo:

```text
is_active = False
↓
login bloqueado
```

---

# DoesNotExist

Se o e-mail não existir:

```python
User.DoesNotExist
```

o backend retorna:

```python
None
```

e o Django entende:

```text
este backend não autenticou
```

---

# MultipleObjectsReturned

Se dois usuários tiverem o mesmo e-mail:

```python
User.MultipleObjectsReturned
```

não sabemos qual conta autenticar.

Por isso também retornamos:

```python
None
```

Esse problema levou diretamente à próxima melhoria:

```text
impedir e-mails duplicados
```

---

# Login funcionando de duas formas

Depois da configuração, testamos:

```text
username + senha ✅
```

e:

```text
e-mail + senha ✅
```

O mesmo `LoginView` continua sendo usado.

Não foi necessário criar outra página de login.

---

# Problema dos e-mails duplicados

O User padrão do Django não exige que:

```text
email
```

seja único.

Então poderia existir:

```text
Usuário A
→ teste@email.com

Usuário B
→ teste@email.com
```

Isso é um problema agora que o e-mail também pode ser usado para login.

---

# Por que precisamos impedir duplicação?

Se houver:

```text
teste@email.com
```

em duas contas, o backend faria:

```python
User.objects.get(email=...)
```

e receberia mais de um resultado.

Resultado:

```text
não sabemos qual usuário autenticar
```

Portanto:

```text
login por e-mail
↓
exige e-mail único na prática
```

---

# Validação no cadastro

Alteramos:

```python
UserRegistrationForm
```

para impedir que um novo usuário use um e-mail já cadastrado.

Também tornamos o e-mail obrigatório.

---

# E-mail obrigatório

Criamos:

```python
email = forms.EmailField(
    label="E-mail",
    required=True,
)
```

Isso faz sentido porque agora o e-mail é usado para:

```text
login
recuperação de senha
```

---

# clean_email() no cadastro

Criamos:

```python
def clean_email(self):
    email = self.cleaned_data["email"].strip()

    if User.objects.filter(
        email__iexact=email
    ).exists():
        raise forms.ValidationError(
            "Este e-mail já está em uso."
        )

    return email
```

---

# O que clean_email() significa?

O Django segue a convenção:

```python
clean_nome_do_campo()
```

Então:

```python
clean_email()
```

é uma validação específica para:

```text
email
```

Ela roda durante:

```python
form.is_valid()
```

---

# exists()

Usamos:

```python
.exists()
```

para descobrir se existe algum usuário com aquele e-mail.

Exemplo:

```python
User.objects.filter(
    email__iexact=email
).exists()
```

Pode retornar:

```text
True
→ já existe

False
→ ainda não existe
```

---

# Validação sem diferenciar maiúsculas

Usamos novamente:

```python
email__iexact=email
```

Isso impede casos como:

```text
teste@email.com
```

e:

```text
TESTE@EMAIL.COM
```

serem cadastrados como se fossem diferentes.

---

# Validação no UserEditForm

Também alteramos:

```python
UserEditForm
```

porque o usuário poderia tentar mudar o próprio e-mail para o e-mail de outra pessoa.

---

# O problema ao editar

Imagine:

```text
Luciano
→ luciano@email.com
```

Se fizéssemos:

```python
User.objects.filter(
    email=email
).exists()
```

o Django encontraria o próprio Luciano.

Então o formulário diria:

```text
Este e-mail já está em uso.
```

mesmo que ele não tenha alterado nada.

---

# exclude()

Para evitar isso, usamos:

```python
.exclude(
    pk=self.instance.pk
)
```

A ideia é:

```text
procure alguém com este e-mail
↓
mas ignore o usuário que estou editando
```

---

# clean_email() no UserEditForm

Ficou conceitualmente assim:

```python
def clean_email(self):
    email = self.cleaned_data["email"].strip()

    if (
        User.objects
        .exclude(pk=self.instance.pk)
        .filter(email__iexact=email)
        .exists()
    ):
        raise forms.ValidationError(
            "Este e-mail já está em uso."
        )

    return email
```

---

# self.instance

Em um ModelForm de edição:

```python
self.instance
```

é o objeto que está sendo editado.

No nosso caso:

```text
self.instance
→ User atual
```

Então:

```python
self.instance.pk
```

é o ID do usuário atual.

---

# pk

`pk` significa:

```text
primary key
```

ou:

```text
chave primária
```

No User padrão do Django, normalmente corresponde ao campo:

```text
id
```

Então:

```python
pk=self.instance.pk
```

é equivalente conceitualmente a:

```text
ID do usuário atual
```

---

# Fluxo da edição

Imagine:

```text
Usuário A
→ a@email.com

Usuário B
→ b@email.com
```

Se A mantiver:

```text
a@email.com
```

temos:

```text
A é excluído da busca
↓
nenhum outro usuário possui a@email.com
↓
permitido ✅
```

Se A tentar usar:

```text
b@email.com
```

temos:

```text
A é excluído
↓
B possui b@email.com
↓
exists() = True
↓
ValidationError ❌
```

---

# Não foi necessária migration

Essas alterações aconteceram apenas nos formulários.

Não mudamos:

```text
models.py
estrutura do banco
```

Então não foi necessário executar:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

# Importante: isso não cria constraint no banco

Nossa proteção atual está no formulário.

Ou seja:

```text
Cadastro pelo formulário
→ protegido ✅

Edição pelo formulário
→ protegida ✅
```

Mas o campo `email` do User padrão ainda não possui necessariamente uma constraint UNIQUE no banco.

Portanto, conceitualmente, ainda seria possível criar duplicação por outros caminhos, como código manual ou certas operações administrativas.

Para o fluxo atual do livro, a validação dos formulários resolve o problema prático que estamos estudando.

---

# Testes realizados

Testamos o cadastro com e-mail duplicado.

Resultado:

```text
Este e-mail já está em uso.
```

Também testamos o sistema após a mudança.

Funcionando:

```text
Login por username ✅
Login por e-mail ✅
Cadastro com e-mail único ✅
Edição com e-mail único ✅
```

---

# Estrutura atual da autenticação do CinePost

```text
LoginView
↓
authenticate()
↓
AUTHENTICATION_BACKENDS
│
├── ModelBackend
│   └── username + senha
│
└── EmailAuthBackend
    └── e-mail + senha
```

E os formulários garantem:

```text
UserRegistrationForm
↓
não permite e-mail já usado

UserEditForm
↓
não permite usar e-mail de outro usuário
```

---

# Resumo mental final

## Backends

```text
AUTHENTICATION_BACKENDS
↓
lista de formas de autenticação
```

---

## ModelBackend

```text
username + senha
```

---

## EmailAuthBackend

```text
e-mail + senha
```

---

## authenticate()

```text
Django tenta backend 1
↓
falhou?
↓
backend 2
↓
...
```

---

## check_password()

```text
senha recebida
↓
comparação com hash
↓
True ou False
```

---

## E-mail único

```text
login por e-mail
↓
precisamos saber exatamente qual User corresponde ao e-mail
↓
não podemos permitir duplicação
```

---

## Cadastro

```text
clean_email()
↓
filter(email__iexact=email)
↓
exists()
↓
já existe?
→ erro
```

---

## Edição

```text
clean_email()
↓
exclude(usuario atual)
↓
procura outro usuário com o mesmo e-mail
↓
existe?
→ erro
```

---

# Estado do capítulo 5 até aqui

```text
Django Messages                    ✅
Mensagens globais no base.html     ✅
Feedback na edit()                 ✅

EmailAuthBackend                   ✅
Login por username                 ✅
Login por e-mail                   ✅

E-mail obrigatório                 ✅
E-mail duplicado no cadastro       ✅ bloqueado
E-mail duplicado na edição         ✅ bloqueado
Comparação case-insensitive        ✅

OAuth 2.0                          ⏳
Python Social Auth                 ⏳
HTTPS em desenvolvimento           ⏳
Login com Google                   ⏳
Pipeline social                    ⏳
Profile automático via Google      ⏳
```