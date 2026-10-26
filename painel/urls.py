from django.urls import path

from . import views

app_name = "painel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("ocorrencias-recentes/", views.ocorrencias_recentes, name="ocorrencias_recentes"),
]