import requests

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Filme


class FilmeCreateForm(forms.ModelForm):

    class Meta:
        model = Filme

        fields = [
            "titulo",
            "url_capa",
            "descricao",
        ]

        widgets = {
            "url_capa": forms.HiddenInput,
        }

    def clean_url_capa(self):

        url = self.cleaned_data["url_capa"]

        extensoes_validas = [
            "jpg",
            "jpeg",
            "png",
        ]

        extensao = url.rsplit(".", 1)[1].lower()

        if extensao not in extensoes_validas:
            raise forms.ValidationError(
                "A URL não possui uma extensão de imagem válida."
            )

        return url

    def save(
        self,
        force_insert=False,
        force_update=False,
        commit=True,
    ):

        filme = super().save(commit=False)

        url_capa = self.cleaned_data["url_capa"]

        nome = slugify(filme.titulo)

        extensao = url_capa.rsplit(".", 1)[1].lower()

        nome_capa = f"{nome}.{extensao}"

        resposta = requests.get(url_capa)

        filme.capa.save(
            nome_capa,
            ContentFile(resposta.content),
            save=False,
        )

        if commit:
            filme.save()

        return filme
