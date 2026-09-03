from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class PublicadosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.Status.PUBLICADO)


class PostFilme(models.Model):

    class Status(models.TextChoices):
        RASCUNHO = "RA", "Rascunho"
        PUBLICADO = "PU", "Publicado"

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date="publicado_em",
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts_filmes",
    )

    comentario = models.TextField()
    nota = models.IntegerField()
    publicado_em = models.DateTimeField(default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
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

    objects = models.Manager()
    publicados = PublicadosManager()

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse(
            "filmes:post_detail",
            kwargs={
                "year": self.publicado_em.year,
                "month": self.publicado_em.month,
                "day": self.publicado_em.day,
                "post": self.slug,
            },
        )
