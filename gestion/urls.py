from django.urls import path

from .views import ProyectoEndpoint


app_name = "gestion"

urlpatterns = [
    path("proyectos/", ProyectoEndpoint.as_view(), name="proyecto-lista"),
    path(
        "proyectos/<int:pk>/",
        ProyectoEndpoint.as_view(),
        name="proyecto-detalle",
    ),
]
