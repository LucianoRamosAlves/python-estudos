from django import template

from ..models import PostFilme


register = template.Library()


@register.simple_tag
def total_posts():
    return PostFilme.publicados.count()