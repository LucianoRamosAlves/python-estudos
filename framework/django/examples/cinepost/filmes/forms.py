from django import forms


class RecomendarPostForm(forms.Form):
    nome = forms.CharField(
        max_length=25,
        label="Seu nome",
    )

    email = forms.EmailField(
        label="Seu e-mail",
    )

    destinatario = forms.EmailField(
        label="E-mail do destinatário",
    )

    comentario = forms.CharField(
        required=False,
        label="Comentário",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Escreva uma mensagem opcional...",
            }
        ),
    )