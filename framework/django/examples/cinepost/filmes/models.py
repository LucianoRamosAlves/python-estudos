from django.db import models
from django.utils import timezone


class PostFilme(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RA", "Rascunho"
        PUBLICADO = "PU", "Publicado"

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    comentario = models.TextField()
    nota = models.IntegerField()
    publicado_em = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.RASCUNHO,
    )

    class Meta:
        ordering = ["-publicado_em"]
        indexes = [
            models.Index(fields=["-publicado_em"]),
        ]

    def __str__(self):
        return self.titulo
