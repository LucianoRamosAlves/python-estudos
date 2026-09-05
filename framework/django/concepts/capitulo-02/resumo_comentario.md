# Django — Comentários na página de detalhes

## View

Na `post_detail`, buscamos apenas comentários ativos e criamos um formulário vazio:

```python
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        PostFilme.publicados,
        slug=post,
        publicado_em__year=year,
        publicado_em__month=month,
        publicado_em__day=day,
    )

    comentarios = post.comentarios.filter(ativo=True)
    form = ComentarioForm()

    return render(
        request,
        "filmes/post/detail.html",
        {
            "post": post,
            "comentarios": comentarios,
            "form": form,
        },
    )
```

## Contando comentários

No template:

```django
{% with comentarios.count as total_comentarios %}
    <h2>
        {{ total_comentarios }}
        comentário{{ total_comentarios|pluralize }}
    </h2>
{% endwith %}
```

`{% with %}` cria uma variável temporária.

`pluralize` ajuda a mostrar:

```text
1 comentário
2 comentários
```

## Listando comentários

```django
{% for comentario in comentarios %}

    <div class="comment">
        <p>
            Comentário {{ forloop.counter }}
            por {{ comentario.nome }}
            em {{ comentario.criado_em }}
        </p>

        {{ comentario.texto|linebreaks }}
    </div>

{% empty %}

    <p>Ainda não existem comentários.</p>

{% endfor %}
```

`forloop.counter` mostra:

```text
1, 2, 3...
```

`{% empty %}` é executado quando não existem comentários.

## Incluindo o formulário

```django
{% include "filmes/post/includes/comment_form.html" %}
```

Assim reutilizamos o mesmo formulário.

## Moderação

A View usa:

```python
post.comentarios.filter(ativo=True)
```

Então:

```text
ativo=True
→ aparece no site

ativo=False
→ continua no banco, mas fica oculto
```

## Fluxo

```text
post_detail
↓
busca post
↓
busca comentários ativos
↓
cria formulário
↓
detail.html
↓
mostra comentários + formulário
```

### Conceitos principais

```django
{% with %}
```

→ variável temporária.

```django
|pluralize
```

→ singular/plural.

```django
{{ forloop.counter }}
```

→ contador do loop.

```django
{% empty %}
```

→ conteúdo exibido quando o `for` está vazio.

```django
{% include %}
```

→ reutiliza outro template.