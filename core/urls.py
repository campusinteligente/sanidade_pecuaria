from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Gestão Sanitária e Alimentar da Pecuária"
admin.site.site_title = "Painel Administrativo"
admin.site.index_title = "Módulos do sistema"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('painel.urls')),
]