from django.db import models

class PostFilme(models.Model):
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    comentario = models.TextField()
    nota = models.IntegerField()

    def __str__(self):
        return self.titulo