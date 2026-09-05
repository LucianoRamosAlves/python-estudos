# Django — Sistema de Comentários com Model, ModelForm e View

## Objetivo

Nesta etapa começamos a criar um sistema de comentários para os posts do CinePost.

A ideia é permitir que visitantes comentem nos posts.

Fluxo geral:

```text
Usuário abre um post
↓
vê os comentários existentes
↓
preenche formulário
↓
envia comentário
↓
Django valida
↓
salva no banco
↓
comentário passa a pertencer ao post
```

---

# 1. Criando o Model `Comentario`

No arquivo:

```text
filmes/models.py
```

criamos:

```python
class Comentario(models.Model):
    post = models.ForeignKey(
        PostFilme,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )

    nome = models.CharField(max_length=80)
    email = models.EmailField()
    texto = models.TextField()

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["criado_em"]
        indexes = [
            models.Index(fields=["criado_em"]),
        ]

    def __str__(self):
        return f"Comentário de {self.nome} em {self.post}"
```

---

# 2. Relação entre PostFilme e Comentario

A parte mais importante é:

```python
post = models.ForeignKey(
    PostFilme,
    on_delete=models.CASCADE,
    related_name="comentarios",
)
```

Isso cria uma relação:

```text
1 PostFilme
↓
muitos Comentarios
```

Ou seja:

```text
PostFilme
├── Comentario 1
├── Comentario 2
├── Comentario 3
└── ...
```

Cada comentário pertence a um único post.

---

# 3. Indo do comentário para o post

Se temos:

```python
comentario
```

podemos acessar:

```python
comentario.post
```

Exemplo:

```python
comentario.post.titulo
```

Pode retornar:

```text
Interestelar
```

---

# 4. Indo do post para os comentários

Como usamos:

```python
related_name="comentarios"
```

podemos fazer:

```python
post.comentarios.all()
```

Isso retorna todos os comentários relacionados ao post.

Exemplo:

```python
post = PostFilme.objects.get(id=5)

post.comentarios.all()
```

---

# 5. `related_name`

Sem:

```python
related_name="comentarios"
```

o Django criaria algo como:

```python
post.comentario_set.all()
```

Mas com:

```python
related_name="comentarios"
```

podemos usar:

```python
post.comentarios.all()
```

que é mais legível.

---

# 6. `on_delete=models.CASCADE`

```python
on_delete=models.CASCADE
```

Significa:

> se o post for excluído, seus comentários também serão excluídos.

Exemplo:

```text
Excluir PostFilme
↓
excluir todos os Comentarios relacionados
```

---

# 7. Campos do Comentario

## Nome

```python
nome = models.CharField(max_length=80)
```

Guarda o nome de quem comentou.

---

## E-mail

```python
email = models.EmailField()
```

Guarda o e-mail de quem comentou.

---

## Texto

```python
texto = models.TextField()
```

Guarda o conteúdo do comentário.

---

## Criado em

```python
criado_em = models.DateTimeField(auto_now_add=True)
```

O Django grava automaticamente a data e hora da criação.

---

## Atualizado em

```python
atualizado_em = models.DateTimeField(auto_now=True)
```

Atualiza automaticamente quando o comentário é alterado.

---

## Ativo

```python
ativo = models.BooleanField(default=True)
```

Permite controlar se o comentário deve aparecer.

```text
ativo=True
→ comentário visível

ativo=False
→ comentário oculto
```

Isso é útil para moderação.

---

# 8. Ordenação padrão

Dentro de:

```python
class Meta:
```

usamos:

```python
ordering = ["criado_em"]
```

Isso faz os comentários aparecerem, por padrão, do mais antigo para o mais novo.

---

# 9. Índice

Também usamos:

```python
indexes = [
    models.Index(fields=["criado_em"]),
]
```

Isso cria um índice no banco para ajudar consultas e ordenações por:

```text
criado_em
```

---

# 10. `__str__`

```python
def __str__(self):
    return f"Comentário de {self.nome} em {self.post}"
```

Isso melhora a forma como o objeto aparece no:

```text
admin
shell
logs
```

Em vez de:

```text
Comentario object (5)
```

fica algo como:

```text
Comentário de Luciano em Interestelar
```

---

# 11. Criando migration

Depois de alterar o Model:

```powershell
python manage.py makemigrations filmes
```

Depois:

```powershell
python manage.py migrate
```

Fluxo:

```text
models.py
↓
makemigrations
↓
arquivo de migration
↓
migrate
↓
banco de dados
```

---

# 12. Registrando Comentario no admin

No:

```text
filmes/admin.py
```

importamos:

```python
from .models import Comentario, PostFilme
```

E criamos:

```python
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "email",
        "post",
        "criado_em",
        "ativo",
    ]

    list_filter = [
        "ativo",
        "criado_em",
        "atualizado_em",
    ]

    search_fields = [
        "nome",
        "email",
        "texto",
    ]
```

---

# 13. `list_display`

```python
list_display = [
    "nome",
    "email",
    "post",
    "criado_em",
    "ativo",
]
```

Define quais colunas aparecem na lista do admin.

---

# 14. `list_filter`

```python
list_filter = [
    "ativo",
    "criado_em",
    "atualizado_em",
]
```

Adiciona filtros laterais.

Exemplo:

```text
Ativo
○ Sim
○ Não
```

---

# 15. `search_fields`

```python
search_fields = [
    "nome",
    "email",
    "texto",
]
```

Permite pesquisar comentários por:

```text
nome
e-mail
conteúdo
```

---

# 16. Admin não precisa de migration

Alterar:

```text
admin.py
```

não muda o banco.

Então:

```text
models.py
→ migration

admin.py
→ sem migration
```

---

# 17. Criando o ModelForm

No:

```text
filmes/forms.py
```

criamos:

```python
from django import forms

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = [
            "nome",
            "email",
            "texto",
        ]
```

---

# 18. Por que usar `ModelForm`?

Antes usamos:

```python
forms.Form
```

para o formulário de recomendação por e-mail.

Aquele formulário:

```text
recebia dados
validava
enviava e-mail
```

mas não estava ligado diretamente a uma tabela.

Agora:

```python
ComentarioForm
```

está ligado ao Model:

```python
Comentario
```

Então usamos:

```python
forms.ModelForm
```

---

# 19. `Form` x `ModelForm`

## Form

```python
forms.Form
```

Usamos quando o formulário é independente do banco.

Exemplos:

```text
recomendação por e-mail
contato
busca
```

---

## ModelForm

```python
forms.ModelForm
```

Usamos quando queremos criar ou editar um objeto do banco.

Exemplos:

```text
criar comentário
editar comentário
criar post
editar post
```

---

# 20. `class Meta` no ModelForm

```python
class Meta:
    model = Comentario
```

Significa:

> este formulário é baseado no Model `Comentario`.

Depois:

```python
fields = [
    "nome",
    "email",
    "texto",
]
```

significa:

> somente estes campos aparecerão no formulário.

---

# 21. Por que não incluímos `post`?

O usuário não precisa escolher em qual post está comentando.

Ele já está dentro daquele post.

Então:

```text
usuário fornece:
nome
email
texto
```

Enquanto:

```text
sistema fornece:
post
ativo
criado_em
atualizado_em
```

---

# 22. Por que não incluímos `ativo`?

Porque o usuário não deve controlar a moderação.

O Model já tem:

```python
ativo = models.BooleanField(default=True)
```

Então todo comentário começa ativo.

Depois um administrador pode mudar para:

```python
ativo = False
```

no admin.

---

# 23. Criando a View para salvar comentários

No:

```text
filmes/views.py
```

criamos:

```python
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import ComentarioForm
from .models import PostFilme


@require_POST
def comentar_post(request, post_id):
    post = get_object_or_404(
        PostFilme.publicados,
        id=post_id,
    )

    comentario = None

    form = ComentarioForm(data=request.POST)

    if form.is_valid():
        comentario = form.save(commit=False)

        comentario.post = post

        comentario.save()

    return render(
        request,
        "filmes/post/comment.html",
        {
            "post": post,
            "form": form,
            "comentario": comentario,
        },
    )
```

---

# 24. `@require_POST`

```python
@require_POST
```

Significa:

> esta View aceita apenas requisições POST.

Então:

```text
POST
→ permitido
```

Mas:

```text
GET
→ 405 Method Not Allowed
```

Isso deixa clara a função da View.

Ela serve apenas para:

```text
receber um comentário
```

---

# 25. Diferença entre 404 e 405

```text
404
→ recurso não existe
```

```text
405
→ recurso existe, mas o método HTTP não é permitido
```

---

# 26. Buscando o PostFilme

```python
post = get_object_or_404(
    PostFilme.publicados,
    id=post_id,
)
```

Se a URL tiver:

```text
/filmes/7/comentar/
```

então:

```python
post_id = 7
```

O Django procura o post publicado de ID 7.

---

# 27. `comentario = None`

```python
comentario = None
```

No começo, nenhum novo comentário foi criado.

Se o formulário for válido, essa variável passa a guardar:

```python
Comentario
```

---

# 28. Recebendo dados via POST

```python
form = ComentarioForm(data=request.POST)
```

O formulário recebe os dados enviados.

Exemplo:

```text
nome=Luciano
email=luciano@email.com
texto=Filme muito bom!
```

---

# 29. Validando

```python
if form.is_valid():
```

O Django valida os dados de acordo com o Model e o ModelForm.

Exemplo:

```text
nome obrigatório?
email válido?
texto preenchido?
```

---

# 30. `form.save()`

Como `ComentarioForm` é um ModelForm, ele possui:

```python
form.save()
```

Isso pode:

```text
criar um objeto Comentario
+
salvar no banco
```

---

# 31. O problema de salvar direto

Se fizermos:

```python
comentario = form.save()
```

o Django tenta salvar imediatamente.

Mas nosso formulário não possui:

```python
post
```

Então ainda falta completar o objeto.

Por isso usamos:

```python
form.save(commit=False)
```

---

# 32. `commit=False`

```python
comentario = form.save(commit=False)
```

Significa:

> crie o objeto `Comentario`, mas não salve no banco ainda.

O objeto passa a existir em memória.

Exemplo conceitual:

```python
comentario.nome = "Luciano"
comentario.email = "luciano@email.com"
comentario.texto = "Filme muito bom!"
comentario.post = ???
```

Ainda falta o post.

---

# 33. Completando o objeto

Depois:

```python
comentario.post = post
```

Agora o comentário sabe a qual post pertence.

---

# 34. Salvando de verdade

Finalmente:

```python
comentario.save()
```

Agora acontece o INSERT no banco.

Fluxo:

```text
POST
↓
ModelForm
↓
is_valid()
↓
save(commit=False)
↓
objeto criado em memória
↓
comentario.post = post
↓
comentario.save()
↓
banco de dados
```

---

# 35. Quando usar `commit=False`

Use quando o formulário não possui todos os dados necessários para salvar o objeto.

Exemplo atual:

```python
comentario = form.save(commit=False)

comentario.post = post

comentario.save()
```

Outro exemplo comum:

```python
publicacao = form.save(commit=False)

publicacao.autor = request.user

publicacao.save()
```

Ou seja:

> o formulário pega os dados do usuário, e o sistema completa o restante.

---

# 36. `save()` existe no ModelForm

Isso é importante:

```python
forms.ModelForm
```

possui:

```python
form.save()
```

porque está ligado a um Model.

Já:

```python
forms.Form
```

não possui esse comportamento automático.

---

# 37. Se o formulário for inválido

Se:

```python
form.is_valid()
```

retornar:

```python
False
```

não salvamos nada.

A variável:

```python
comentario
```

continua:

```python
None
```

E o template recebe o próprio formulário com os erros.

---

# 38. Criando a URL

No:

```text
filmes/urls.py
```

adicionamos:

```python
path(
    "<int:post_id>/comentar/",
    views.comentar_post,
    name="comentar_post",
),
```

Exemplo:

```text
/filmes/7/comentar/
```

gera:

```python
post_id = 7
```

para a View.

---

# 39. Estrutura atual da funcionalidade

```text
filmes/
│
├── models.py
│   └── Comentario
│
├── forms.py
│   └── ComentarioForm
│
├── views.py
│   └── comentar_post
│
├── urls.py
│   └── comentar_post
│
├── admin.py
│   └── ComentarioAdmin
│
└── templates/
    └── filmes/
        └── post/
            └── comment.html
```

O `comment.html` ainda será criado.

---

# 40. Responsabilidade de cada parte

## Model

```text
define estrutura do comentário
salva no banco
define relação com PostFilme
```

## ModelForm

```text
gera campos
valida dados
cria objeto Comentario
```

## View

```text
recebe POST
valida formulário
completa o objeto
salva no banco
```

## URL

```text
liga endereço à View
```

## Admin

```text
permite moderar comentários
```

---

# 41. Mapa mental completo

```text
PostFilme
│
└── comentarios
    │
    ├── Comentario
    ├── Comentario
    └── Comentario
```

Quando o usuário comenta:

```text
POST
↓
comentar_post()
↓
ComentarioForm(request.POST)
↓
is_valid()
↓
form.save(commit=False)
↓
Comentario criado em memória
↓
comentario.post = post
↓
comentario.save()
↓
SQLite
```

---

# 42. Conceitos importantes para decorar

## ForeignKey

```python
models.ForeignKey(...)
```

Cria relação entre modelos.

---

## related_name

```python
related_name="comentarios"
```

Permite:

```python
post.comentarios.all()
```

---

## ModelForm

```python
forms.ModelForm
```

Cria formulário baseado em Model.

---

## `fields`

```python
fields = [
    "nome",
    "email",
    "texto",
]
```

Controla quais campos entram no formulário.

---

## `@require_POST`

```python
@require_POST
```

Permite somente POST.

---

## `form.is_valid()`

Valida os dados.

---

## `form.save(commit=False)`

Cria o objeto sem salvar ainda.

---

## completar objeto

```python
comentario.post = post
```

Adiciona informação que não veio do formulário.

---

## salvar

```python
comentario.save()
```

Salva de verdade no banco.

---

# 43. Resumo final

A funcionalidade de comentários segue este fluxo:

```text
Model Comentario
↓
Migration
↓
Admin
↓
ModelForm
↓
POST
↓
View
↓
Validação
↓
commit=False
↓
associar PostFilme
↓
save()
↓
Banco de dados
```

A principal ideia dessa etapa é:

> O `ModelForm` cria e valida dados com base em um Model.

> O `commit=False` permite criar o objeto sem salvá-lo imediatamente.

> Isso é útil quando precisamos adicionar informações que não vieram do formulário.

No CinePost:

```text
usuário fornece:
nome
email
texto
```

E o sistema fornece:

```text
post
ativo
datas
```

Depois o comentário completo é salvo no banco.