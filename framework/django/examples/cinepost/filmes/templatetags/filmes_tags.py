from django import template

from ..models import PostFilme

from django.db.models import Count, Q



register = template.Library()


@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()

@register.inclusion_tag("filmes/post/ultimos_posts.html")
def mostrar_ultimos_posts(quantidade=5):
    ultimos_posts = PostFilme.publicados.order_by(
        "-publicado_em"
    )[:quantidade]

    return {
        "ultimos_posts": ultimos_posts
    }


@register.simple_tag
def posts_mais_comentados(quantidade=5):
    return (
        PostFilme.publicados
        .annotate(
            total_comentarios=Count(
                "comentarios",
                filter=Q(comentarios__ativo=True),
            )
        )
        .order_by("-total_comentarios")[:quantidade]
    )