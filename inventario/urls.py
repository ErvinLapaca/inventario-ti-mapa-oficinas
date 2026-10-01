from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("personas/<int:persona_id>/mover/", views.mover_persona, name="mover_persona"),
    path("personas/<int:persona_id>/mover-mapa/", views.mover_persona_ajax, name="mover_persona_ajax"),
]
