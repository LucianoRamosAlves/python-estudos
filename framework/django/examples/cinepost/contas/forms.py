from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = [
            "username",
            "first_name",
            "email",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")

        return email


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="E-mail",
        required=True,
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if (
            User.objects.exclude(pk=self.instance.pk)
            .filter(email__iexact=email)
            .exists()
        ):
            raise forms.ValidationError("Este e-mail já está em uso.")

        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = [
            "date_of_birth",
            "photo",
        ]
