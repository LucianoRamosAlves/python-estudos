from django.shortcuts import get_object_or_404, render

from .models import PostFilme

from django.views.generic import ListView

from .forms import RecomendarPostForm, ComentarioForm

from django.core.mail import send_mail

from django.views.decorators.http import require_POST


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
    post = get_object_or_404(
        PostFilme.publicados,
        id=post_id,
    )

    enviado = False

    if request.method == "POST":
        form = RecomendarPostForm(request.POST)

        if form.is_valid():
            dados = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            assunto = (
                f"{dados['nome']} ({dados['email']}) "
                f"recomenda o post {post.titulo}"
            )

            mensagem = (
                f"Veja {post.titulo} em:\n"
                f"{post_url}\n\n"
                f"Comentário de {dados['nome']}:\n"
                f"{dados['comentario']}"
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=None,
                recipient_list=[dados["destinatario"]],
            )

            enviado = True

    else:
        form = RecomendarPostForm()

    return render(
        request,
        "filmes/post/share.html",
        {
            "post": post,
            "form": form,
            "enviado": enviado,
        },
    )


@require_POST
def comentar_post(request, post_id):
    post = get_object_or_404(
        PostFilme.publicados,
        id=post_id,
    )

    comentario = None

    form = ComentarioForm(data=request.POST)

    if form.is_valid():
        comentario = form.save(commit=False)

        comentario.post = post

        comentario.save()

    return render(
        request,
        "filmes/post/comment.html",
        {
            "post": post,
            "form": form,
            "comentario": comentario,
        },
    )

