from django.urls import include, path

from . import views

app_name = "contas"


urlpatterns = [
    path(
        "",
        include("django.contrib.auth.urls"),
    ),
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
]
