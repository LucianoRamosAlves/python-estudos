# Django ORM — Manager Personalizado

## O que é um Manager?

Todo model do Django possui um **Manager**.

O Manager é a porta de entrada que usamos para fazer consultas no banco de dados.

Por padrão, o Django cria:

```python
objects
```

Por isso podemos fazer:

```python
PostFilme.objects.all()
```

Ou:

```python
PostFilme.objects.filter(nota__gte=8)
```

Podemos pensar assim:

```text
PostFilme
    ↓
objects
    ↓
QuerySet
    ↓
Banco de dados
```

---

# Manager padrão

O Manager padrão normalmente é:

```python
objects = models.Manager()
```

Então:

```python
PostFilme.objects.all()
```

significa:

> Pegue todos os objetos `PostFilme`.

Exemplo:

```python
PostFilme.objects.filter(nota__gte=8)
```

Significa:

> Pegue todos os posts com nota maior ou igual a 8.

---

# Por que criar um Manager personalizado?

Imagine que no CinePost precisamos buscar **posts publicados** o tempo inteiro.

Sem um Manager personalizado, teríamos que repetir:

```python
PostFilme.objects.filter(
    status=PostFilme.Status.PUBLICADO
)
```

em várias partes do projeto.

Podemos criar um Manager chamado:

```python
publicados
```

Assim podemos fazer simplesmente:

```python
PostFilme.publicados.all()
```

Isso já significa:

> Pegue somente os posts publicados.

---

# Criando o PublicadosManager

```python
class PublicadosManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=self.model.Status.PUBLICADO
        )
```

Vamos entender cada parte.

---

## `models.Manager`

```python
class PublicadosManager(models.Manager):
```

Estamos criando um novo Manager baseado no Manager padrão do Django.

É como dizer:

> Quero criar meu próprio tipo de atendente para consultar o banco.

---

# `get_queryset()`

```python
def get_queryset(self):
```

Esse método define qual QuerySet esse Manager deve entregar.

Podemos pensar:

> Quando alguém usar `publicados`, quais registros devem ser considerados?

---

# `super().get_queryset()`

```python
super().get_queryset()
```

Isso pega o QuerySet normal do model.

Ou seja:

```text
Todos os PostFilme
```

Depois adicionamos:

```python
.filter(
    status=self.model.Status.PUBLICADO
)
```

Então temos:

```text
Todos os posts
       ↓
filtrar
       ↓
status = PUBLICADO
       ↓
Somente posts publicados
```

---

# O que é `self.model`?

Dentro do Manager:

```python
self.model
```

representa o model ao qual aquele Manager está conectado.

No nosso caso:

```text
self.model
    ↓
PostFilme
```

Portanto:

```python
self.model.Status.PUBLICADO
```

é equivalente, neste caso, a:

```python
PostFilme.Status.PUBLICADO
```

Usar `self.model` deixa o Manager menos dependente do nome específico do model.

---

# Colocando os Managers no PostFilme

Dentro do nosso model:

```python
objects = models.Manager()

publicados = PublicadosManager()
```

Agora o `PostFilme` possui dois Managers.

---

## `objects`

```python
PostFilme.objects
```

É o Manager geral.

Exemplo:

```python
PostFilme.objects.all()
```

Retorna:

> Todos os posts.

---

## `publicados`

```python
PostFilme.publicados
```

É nosso Manager personalizado.

Exemplo:

```python
PostFilme.publicados.all()
```

Retorna:

> Somente posts cujo status é PUBLICADO.

---

# Comparação

| Código | Resultado |
|---|---|
| `PostFilme.objects.all()` | Todos os posts |
| `PostFilme.publicados.all()` | Somente os publicados |
| `PostFilme.publicados.count()` | Quantidade de publicados |
| `PostFilme.publicados.exists()` | Verifica se existe algum publicado |
| `PostFilme.publicados.filter(nota__gte=8)` | Publicados com nota 8 ou maior |

---

# Podemos continuar usando filter()

O Manager personalizado continua retornando um QuerySet.

Por isso podemos fazer:

```python
PostFilme.publicados.filter(
    nota__gte=8
)
```

O Manager já colocou:

```text
status = PUBLICADO
```

E nosso `filter()` adicionou:

```text
nota >= 8
```

Então a consulta significa:

```text
status = PUBLICADO
        E
nota >= 8
```

---

# Outro exemplo

```python
PostFilme.publicados.filter(
    titulo__icontains="matrix"
)
```

Significa:

> Pegue os posts publicados cujo título contém "matrix".

O Manager adiciona automaticamente:

```text
status = PUBLICADO
```

E nós adicionamos:

```text
titulo contém "matrix"
```

---

# Código do nosso CinePost

```python
from django.db import models
from django.utils import timezone
from django.conf import settings


class PublicadosManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=self.model.Status.PUBLICADO
        )


class PostFilme(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RA", "Rascunho"
        PUBLICADO = "PU", "Publicado"

    titulo = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250)

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts_filmes",
    )

    comentario = models.TextField()

    nota = models.IntegerField()

    publicado_em = models.DateTimeField(
        default=timezone.now
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.RASCUNHO,
    )

    objects = models.Manager()

    publicados = PublicadosManager()

    class Meta:
        ordering = ["-publicado_em"]

        indexes = [
            models.Index(
                fields=["-publicado_em"]
            ),
        ]

    def __str__(self):
        return self.titulo
```

---

# Testando no Django Shell

Abra:

```bash
python manage.py shell
```

Importe:

```python
from filmes.models import PostFilme
```

---

## Ver todos

```python
PostFilme.objects.all()
```

---

## Ver somente publicados

```python
PostFilme.publicados.all()
```

---

## Publicados com nota 8 ou maior

```python
PostFilme.publicados.filter(
    nota__gte=8
)
```

---

## Contar publicados

```python
PostFilme.publicados.count()
```

---

## Verificar se existe algum publicado

```python
PostFilme.publicados.exists()
```

---

# Analogia

Podemos imaginar que o Manager é um atendente do arquivo.

## `objects`

```python
PostFilme.objects
```

É o atendente geral:

> "Posso procurar qualquer post."

---

## `publicados`

```python
PostFilme.publicados
```

É um atendente especializado:

> "Eu só trabalho com posts publicados."

Por isso:

```python
PostFilme.objects.all()
```

significa:

> Todos.

Enquanto:

```python
PostFilme.publicados.all()
```

significa:

> Somente publicados.

---

# Resumo

```text
PostFilme
    │
    ├── objects
    │      ↓
    │   Todos os posts
    │
    └── publicados
           ↓
       Somente PUBLICADOS
```

O Manager personalizado serve para criar **consultas reutilizáveis**.

Em vez de repetir:

```python
PostFilme.objects.filter(
    status=PostFilme.Status.PUBLICADO
)
```

podemos escrever:

```python
PostFilme.publicados.all()
```

## Para decorar

```python
objects = models.Manager()
```

> Manager normal.

```python
publicados = PublicadosManager()
```

> Nosso Manager personalizado.

```python
def get_queryset(self):
```

> Define qual QuerySet o Manager vai entregar.

```python
super().get_queryset()
```

> Começa com o QuerySet normal.

```python
.filter(status=self.model.Status.PUBLICADO)
```

> Limita o QuerySet aos posts publicados.

### Resultado final

```python
PostFilme.objects.all()
```

**Todos os posts.**

```python
PostFilme.publicados.all()
```

**Somente os posts publicados.**