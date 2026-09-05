from django.urls import path

from . import views

app_name = "filmes"


urlpatterns = [
    path(
        "",
        views.PostListView.as_view(),
        name="post_list",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path(
        "<int:post_id>/recomendar/",
        views.recomendar_post,
        name="recomendar_post",
    ),
    path(
        "<int:post_id>/comentar/",
        views.comentar_post,
        name="comentar_post",
    ),
]
