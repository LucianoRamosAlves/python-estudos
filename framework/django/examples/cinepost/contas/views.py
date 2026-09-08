from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


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
