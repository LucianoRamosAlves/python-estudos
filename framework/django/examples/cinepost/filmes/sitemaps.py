from django.contrib.sitemaps import Sitemap

from .models import PostFilme


class PostFilmeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return PostFilme.publicados.all()

    def lastmod(self, obj):
        return obj.atualizado_em