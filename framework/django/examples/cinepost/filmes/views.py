from django.shortcuts import get_object_or_404, render

from .models import PostFilme

from django.views.generic import ListView

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