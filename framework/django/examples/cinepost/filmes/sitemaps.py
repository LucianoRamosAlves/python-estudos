from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag

from .models import PostFilme


class PostFilmeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return PostFilme.publicados.all()

    def lastmod(self, obj):
        return obj.atualizado_em

class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse(
            "filmes:post_list_by_tag",
            kwargs={
                "tag_slug": obj.slug,
            },
        )