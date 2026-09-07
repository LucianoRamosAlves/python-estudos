from django import template

from ..models import PostFilme


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