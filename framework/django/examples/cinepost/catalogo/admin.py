from django.contrib import admin

from .models import Filme


@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):

    list_display = [
        "titulo",
        "slug",
        "capa",
        "criado_em",
    ]

    list_filter = [
        "criado_em",
    ]