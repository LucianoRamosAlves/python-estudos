from django.contrib import admin
from .models import PostFilme, Comentario

@admin.register(PostFilme)
class PostFilmeAdmin(admin.ModelAdmin):
    list_display = [
        "titulo",
        "slug",
        "autor",
        "publicado_em",
        "status",
    ]

    list_filter = [
        "status",
        "criado_em",
        "publicado_em",
        "autor",
    ]

    search_fields = [
        "titulo",
        "comentario",
    ]

    prepopulated_fields = {
        "slug": ("titulo",),
    }

    raw_id_fields = [
        "autor",
    ]

    date_hierarchy = "publicado_em"

    ordering = [
        "status",
        "publicado_em",
    ]

    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        "nome",
        "email",
        "post",
        "criado_em",
        "ativo",
    ]

    list_filter = [
        "ativo",
        "criado_em",
        "atualizado_em",
    ]

    search_fields = [
        "nome",
        "email",
        "texto",
    ]