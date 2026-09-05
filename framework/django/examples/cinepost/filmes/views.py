from django.shortcuts import get_object_or_404, render

from .models import PostFilme

from django.views.generic import ListView

from .forms import RecomendarPostForm

class PostListView(ListView):
    template_name = "filmes/post/list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        return PostFilme.publicados.all()



def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        PostFilme.publicados,
        slug=post,
        publicado_em__year=year,
        publicado_em__month=month,
        publicado_em__day=day,
    )

    return render(
        request,
        "filmes/post/detail.html",
        {"post": post},
    )

def recomendar_post(request, post_id):
    # Busca somente um post publicado
    post = get_object_or_404(
        PostFilme.publicados,
        id=post_id,
    )

    if request.method == "POST":
        # O usuário enviou o formulário
        form = RecomendarPostForm(request.POST)

        if form.is_valid():
            # Dados passaram pela validação
            dados = form.cleaned_data

            # Depois colocaremos aqui o envio do e-mail

    else:
        # Usuário apenas abriu a página
        form = RecomendarPostForm()

    return render(
        request,
        "filmes/post/share.html",
        {
            "post": post,
            "form": form,
        },
    )