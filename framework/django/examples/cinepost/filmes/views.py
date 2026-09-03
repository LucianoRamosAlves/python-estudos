from django.shortcuts import get_object_or_404, render

from .models import PostFilme


def post_list(request):
    posts = PostFilme.publicados.all()

    return render(
        request,
        "filmes/post/list.html",
        {"posts": posts},
    )


def post_detail(request, id):
    post = get_object_or_404(
        PostFilme.publicados,
        id=id,
        # post=get_object_or_404(
        #     PostFilme,
        #     id=id,
        #     status=PostFilme.Status.PUBLICADO, a gente esta usand o nosso manager acima
        # ),
    )

    return render(
        request,
        "filmes/post/detail.html",
        {"post": post},
    )
