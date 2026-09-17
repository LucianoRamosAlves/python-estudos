from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Filme(models.Model):

    url_capa = models.URLField(
    max_length=2000,
    blank=True,
)

    adicionado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="filmes_adicionados",
        on_delete=models.CASCADE,
    )

    titulo = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=200,
        blank=True,
    )

    capa = models.ImageField(
        upload_to="filmes/%Y/%m/%d/"
    )

    descricao = models.TextField(
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    usuarios_curtiram = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name="filmes_curtidos",
    blank=True,
)


    class Meta:

        indexes = [
            models.Index(
                fields=["-criado_em"]
            ),
        ]

        ordering = [
            "-criado_em"
        ]


    def __str__(self):
        return self.titulo


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.titulo)

        super().save(*args, **kwargs)