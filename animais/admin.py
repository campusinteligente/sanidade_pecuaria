from django.contrib import admin

from .models import Animal, Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("identificacao", "especie", "raca", "sexo", "setor", "ativo")
    list_filter = ("especie", "sexo", "ativo", "setor")
    search_fields = ("identificacao", "raca")
