from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            dados = form.cleaned_data

            user = authenticate(
                request,
                username=dados["username"],
                password=dados["password"],
            )

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponse("Autenticado com sucesso.")

                return HttpResponse("Conta desativada.")

            return HttpResponse("Usuário ou senha inválidos.")

    else:
        form = LoginForm()

    return render(
        request,
        "contas/login.html",
        {
            "form": form,
        },
    )


@login_required
def dashboard(request):
    return render(
        request,
        "contas/dashboard.html",
    )

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(
                commit=False
            )

            new_user.set_password(
                user_form.cleaned_data["password"]
            )

            new_user.save()

            return render(
                request,
                "contas/register_done.html",
                {
                    "new_user": new_user,
                },
            )

    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        "contas/register.html",
        {
            "user_form": user_form,
        },
    )
