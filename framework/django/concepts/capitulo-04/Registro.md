# Django — Resumo da Parte de Registro de Usuários

## Objetivo desta etapa

Até aqui, o CinePost já permitia:

```text
login
logout
troca de senha
recuperação de senha
```

Mas todos esses recursos partiam da ideia de que o usuário já existia no banco.

Agora começamos a permitir que um visitante crie a própria conta.

O fluxo geral do registro ficou:

```text
Visitante
↓
/contas/register/
↓
preenche formulário
↓
Django valida
↓
cria objeto User
↓
trata a senha com set_password()
↓
salva no banco
↓
conta criada
↓
usuário pode fazer login
```

---

# 1. UserRegistrationForm

Criamos um novo formulário em:

```text
contas/forms.py
```

Chamado:

```python
UserRegistrationForm
```

Ele é diferente do antigo `LoginForm`.

---

# 2. LoginForm x UserRegistrationForm

## LoginForm

Usávamos:

```python
forms.Form
```

porque o login apenas recebe:

```text
username
password
```

e tenta autenticar uma conta que já existe.

---

## UserRegistrationForm

Agora usamos:

```python
forms.ModelForm
```

porque vamos realmente criar um registro no Model de usuário.

Mentalmente:

```text
LoginForm
→ verifica usuário existente
```

```text
UserRegistrationForm
→ cria novo usuário
```

---

# 3. get_user_model()

No formulário importamos:

```python
from django.contrib.auth import get_user_model
```

e usamos:

```python
model = get_user_model()
```

Isso significa:

```text
Django, me dê o Model de usuário usado por este projeto.
```

Hoje o CinePost usa o User padrão do Django.

Mas essa forma é melhor do que importar diretamente:

```python
from django.contrib.auth.models import User
```

porque se futuramente o projeto usar um usuário personalizado, o código continua mais compatível.

---

# 4. Campos do formulário

No ModelForm escolhemos campos do User:

```text
username
first_name
email
```

Esses campos já pertencem ao Model de usuário do Django.

Além deles, criamos manualmente:

```text
password
password2
```

---

# 5. Por que password2?

O campo:

```text
password2
```

não existe no Model `User`.

Ele existe apenas no formulário.

Serve para confirmar a senha.

Exemplo:

```text
Senha:
123456

Repita a senha:
123456
```

Assim podemos evitar erros de digitação.

---

# 6. PasswordInput

Nos dois campos de senha usamos:

```python
forms.PasswordInput
```

Isso faz o navegador renderizar campos do tipo:

```html
<input type="password">
```

e mostrar:

```text
••••••••
```

em vez da senha digitada.

---

# 7. clean_password2()

Criamos:

```python
def clean_password2(self):
```

Esse método é executado durante a validação do formulário.

A ideia é:

```text
password
vs
password2
```

Se forem diferentes:

```text
formulário inválido
```

e geramos:

```python
forms.ValidationError(...)
```

---

# 8. clean_<campo>()

Esse padrão do Django é importante:

```python
clean_nome_do_campo()
```

Exemplos possíveis:

```python
clean_email()
clean_username()
clean_password2()
```

Esses métodos servem para validar campos específicos.

---

# 9. clean() geral

O Django também possui:

```python
clean()
```

Esse método pode ser usado quando precisamos validar o formulário como um todo.

Mas neste caso usamos:

```python
clean_password2()
```

porque queremos validar especificamente a confirmação da senha.

---

# 10. Validação de username único

Não precisamos escrever manualmente uma consulta para verificar se o username já existe.

O campo `username` do User do Django já possui uma regra de unicidade.

Então:

```text
username já existe
↓
ModelForm valida
↓
formulário mostra erro
```

---

# 11. View register

Depois criamos uma view chamada:

```python
register
```

Ela é responsável pelo cadastro do usuário.

O fluxo segue o mesmo padrão que já vimos em outros formulários Django.

---

# 12. GET no register

Quando o usuário acessa:

```text
/contas/register/
```

pela primeira vez, temos normalmente:

```text
GET
```

Então criamos:

```python
UserRegistrationForm()
```

vazio.

Fluxo:

```text
GET
↓
formulário vazio
↓
register.html
```

---

# 13. POST no register

Quando o usuário envia o cadastro:

```text
POST
```

criamos:

```python
UserRegistrationForm(request.POST)
```

Agora o formulário recebe os dados enviados.

---

# 14. is_valid()

Depois fazemos:

```python
user_form.is_valid()
```

O Django executa várias validações.

Entre elas:

```text
campos obrigatórios
username único
formato de e-mail
clean_password2()
```

Se houver erro:

```text
o formulário volta para a página
com os erros
```

Se estiver tudo válido:

```text
podemos criar o usuário
```

---

# 15. save(commit=False)

Essa foi uma das partes mais importantes.

Usamos:

```python
new_user = user_form.save(commit=False)
```

Isso significa:

```text
crie o objeto User em memória
mas ainda não salve no banco
```

Mentalmente:

```text
ModelForm
↓
objeto User criado
↓
AINDA não salvo
```

---

# 16. Por que usamos commit=False?

Porque antes de salvar precisamos tratar a senha corretamente.

Se salvássemos imediatamente:

```python
user_form.save()
```

não teríamos feito o tratamento de senha da forma que queremos nesta implementação.

Então fazemos:

```text
cria User
↓
não salva
↓
trata senha
↓
salva depois
```

---

# 17. set_password()

Depois usamos:

```python
new_user.set_password(...)
```

Esse é um conceito essencial.

Nunca devemos tratar senha como um campo comum.

Não devemos simplesmente fazer:

```python
new_user.password = "123456"
```

A senha precisa passar pelo sistema de hashing do Django.

Por isso usamos:

```python
set_password()
```

---

# 18. O que set_password() faz?

Ele pega a senha digitada e transforma em um valor seguro antes de armazenar.

Fluxo:

```text
senha digitada
↓
set_password()
↓
hash
↓
banco de dados
```

Então o banco não guarda algo como:

```text
123456
```

Ele guarda uma representação hash.

---

# 19. Senha em texto puro x hash

Texto puro seria:

```text
123456
```

Isso seria extremamente inseguro.

Hash é uma transformação usada para armazenar a senha de forma apropriada.

O Django compara senhas usando seu sistema de hashers.

---

# 20. O Django não recupera a senha original

Assim como vimos no reset de senha, o Django não fica armazenando a senha original para depois mostrá-la.

Ele trabalha com hash.

Por isso:

```text
esqueceu a senha
→ cria uma nova
```

e não:

```text
esqueceu a senha
→ Django mostra a antiga
```

---

# 21. PASSWORD_HASHERS

O Django possui uma configuração chamada:

```python
PASSWORD_HASHERS
```

Ela define quais algoritmos de hash podem ser utilizados.

O primeiro da lista é o principal usado para novas senhas.

O livro cita algoritmos como:

```text
PBKDF2
PBKDF2SHA1
Argon2
BCrypt
Scrypt
```

O ponto principal para esta etapa é entender:

```text
não precisamos implementar hashing manualmente
```

O Django já faz isso.

---

# 22. new_user.save()

Depois de tratar a senha:

```python
new_user.save()
```

Agora sim o usuário é salvo no banco.

Fluxo:

```text
UserRegistrationForm
↓
save(commit=False)
↓
User em memória
↓
set_password()
↓
hash
↓
save()
↓
User no banco
```

---

# 23. register.html

Criamos um template para o formulário de cadastro:

```text
contas/templates/contas/register.html
```

Ele recebe:

```text
user_form
```

e mostra os campos do cadastro.

O formulário utiliza:

```text
POST
```

e precisa de:

```django
{% csrf_token %}
```

---

# 24. register_done.html

Também criamos:

```text
contas/templates/contas/register_done.html
```

Essa página aparece quando a conta foi criada com sucesso.

Ela pode mostrar algo como:

```text
Bem-vindo, Luciano!

Sua conta foi criada com sucesso.
```

e oferece um link para login.

---

# 25. new_user no template

Depois do cadastro, a view envia para o template:

```text
new_user
```

Esse objeto representa o usuário que acabou de ser criado.

Por isso podemos acessar informações como:

```django
{{ new_user.first_name }}
```

---

# 26. URL register

Adicionamos uma URL:

```text
/contas/register/
```

ligada à:

```python
views.register
```

com o nome:

```text
register
```

Então podemos gerar links usando:

```django
{% url "register" %}
```

---

# 27. Link de cadastro no login

Também adicionamos no:

```text
registration/login.html
```

um link para quem ainda não possui conta.

Exemplo conceitual:

```text
Ainda não possui uma conta?
Cadastre-se.
```

Fluxo:

```text
Login
↓
Cadastre-se
↓
/contas/register/
```

---

# 28. Fluxo completo do cadastro

```text
Visitante acessa:

/contas/register/

↓
GET

↓
UserRegistrationForm vazio

↓
register.html

↓
usuário preenche:
username
nome
e-mail
senha
confirmação

↓
POST

↓
UserRegistrationForm(request.POST)

↓
is_valid()

↓
clean_password2()

↓
username é único?

↓
dados válidos

↓
save(commit=False)

↓
User criado em memória

↓
set_password()

↓
senha convertida para hash

↓
new_user.save()

↓
User salvo no banco

↓
register_done.html

↓
usuário clica em Entrar

↓
LoginView
```

---

# 29. O ponto mais importante desta seção

O núcleo do registro é:

```python
new_user = user_form.save(commit=False)

new_user.set_password(
    user_form.cleaned_data["password"]
)

new_user.save()
```

Mentalmente:

```text
crio o usuário sem salvar
↓
trato a senha corretamente
↓
salvo o usuário
```

---

# 30. Por que não usamos UserCreationForm?

O Django também oferece um formulário pronto chamado:

```python
UserCreationForm
```

Ele é semelhante ao que construímos.

Mas o livro cria um formulário próprio primeiro para ensinar:

```text
ModelForm
clean_password2()
commit=False
set_password()
```

Então essa implementação também tem objetivo didático.

---

# 31. Registro x autenticação

É importante diferenciar.

## Registro

```text
cria uma conta nova
```

Usa:

```text
UserRegistrationForm
register
set_password()
```

---

## Login

```text
entra em uma conta existente
```

Usa:

```text
LoginView
AuthenticationForm
```

---

# 32. Registro x perfil

Também são coisas diferentes.

## Registro

Cria:

```text
User
```

com informações básicas.

Exemplo:

```text
username
first_name
email
password
```

---

## Perfil

Será a próxima etapa.

O perfil poderá guardar informações extras que não fazem parte diretamente do User padrão.

Exemplo conceitual:

```text
foto
data de nascimento
biografia
```

---

# 33. O que já temos funcionando agora

Até essa parte do registro:

```text
✅ formulário de cadastro
✅ UserRegistrationForm
✅ get_user_model()
✅ ModelForm
✅ password
✅ password2
✅ clean_password2()
✅ validação de username
✅ view register
✅ GET
✅ POST
✅ is_valid()
✅ save(commit=False)
✅ set_password()
✅ hashing
✅ save()
✅ register.html
✅ register_done.html
✅ URL /contas/register/
✅ link de cadastro no login
```

---

# Resumo mental

## Formulário

```text
UserRegistrationForm
↓
username
nome
e-mail
senha
confirmação
```

## Validação

```text
is_valid()
↓
username válido?
↓
senhas iguais?
```

## Criação

```text
save(commit=False)
↓
set_password()
↓
save()
```

## Resultado

```text
conta criada
↓
register_done.html
↓
login
```

---

# Forma mais curta de lembrar

```text
REGISTER

Formulário
↓
validar
↓
criar User sem salvar
↓
tratar senha
↓
salvar
↓
login
```

Ou ainda:

```text
UserRegistrationForm
→ clean_password2()
→ commit=False
→ set_password()
→ save()
```

Esse é o coração da parte de registro.