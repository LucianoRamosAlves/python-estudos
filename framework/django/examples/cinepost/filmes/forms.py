from django import forms

from .models import Comentario


class RecomendarPostForm(forms.Form):
    nome = forms.CharField(
        max_length=25,
        label="Seu nome",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        label="Seu e-mail",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    destinatario = forms.EmailField(
        label="E-mail do destinatário",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
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
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "texto": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }