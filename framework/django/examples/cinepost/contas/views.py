from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import (
    ProfileEditForm,
    UserEditForm,
    UserRegistrationForm,
)
from .models import Profile


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
            new_user = user_form.save()

            Profile.objects.create(user=new_user)

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


@login_required
def edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST,
        )

        profile_form = ProfileEditForm(
            instance=profile,
            data=request.POST,
            files=request.FILES,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Perfil atualizado com sucesso.",
            )

            return redirect("edit")

        else:
            messages.error(
                request,
                "Não foi possível atualizar o perfil. Verifique os campos.",
            )

    else:
        user_form = UserEditForm(instance=request.user)

        profile_form = ProfileEditForm(instance=profile)
        

    return render(
        request,
        "contas/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
