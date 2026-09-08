from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import PostFilme


class UltimosPostsFeed(Feed):
    title = "CinePost"

    link = reverse_lazy("filmes:post_list")

    description = "Últimas publicações do CinePost."

    def items(self):
        return PostFilme.publicados.order_by("-publicado_em")[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords(
            item.comentario,
            30,
        )

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publicado_em

    def item_updateddate(self, item):
        return item.atualizado_em
