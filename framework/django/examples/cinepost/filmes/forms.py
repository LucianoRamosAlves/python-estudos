from django import forms

from .models import Comentario


class RecomendarPostForm(forms.Form):
    nome = forms.CharField(
        max_length=25,
        label="Seu nome",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu nome",
            }
        ),
    )

    email = forms.EmailField(
        label="Seu e-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
            }
        ),
    )

    destinatario = forms.EmailField(
        label="E-mail do destinatário",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "destinatario@email.com",
            }
        ),
    )

    comentario = forms.CharField(
        required=False,
        label="Comentário",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Escreva uma mensagem opcional...",
            }
        ),
    )


class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario

        fields = [
            "nome",
            "email",
            "texto",
        ]

        labels = {
            "nome": "Seu nome",
            "email": "Seu e-mail",
            "texto": "Comentário",
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu nome",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "seu@email.com",
                }
            ),

            "texto": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Escreva seu comentário...",
                }
            ),
        }


class BuscaForm(forms.Form):
    query = forms.CharField(
        label="Buscar",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite o nome de um filme, tag ou palavra...",
            }
        ),
    )