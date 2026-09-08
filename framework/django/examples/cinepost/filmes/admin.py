from django.contrib import admin

from .models import Comentario, PostFilme


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
        "autor__username",
    ]

    prepopulated_fields = {
        "slug": ("titulo",),
    }

    raw_id_fields = [
        "autor",
    ]

    list_select_related = [
        "autor",
    ]

    date_hierarchy = "publicado_em"

    ordering = [
        "status",
        "-publicado_em",
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
        "post__titulo",
    ]

    list_select_related = [
        "post",
    ]

    ordering = [
        "-criado_em",
    ]