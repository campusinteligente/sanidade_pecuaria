from django.urls import path

from . import views

urlpatterns = [
    path("definir-setor/", views.definir_setor, name="definir_setor"),
]
