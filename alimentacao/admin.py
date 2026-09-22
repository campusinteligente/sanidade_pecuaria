from django.contrib import admin

from .models import (
    Alimentacao,
    ConsumoSetor,
    Dieta,
    DietaProduto,
    ProdutoAlimentar,
    TipoAlimentacao,
)


@admin.register(TipoAlimentacao)
class TipoAlimentacaoAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(ProdutoAlimentar)
class ProdutoAlimentarAdmin(admin.ModelAdmin):
    list_display = ("nome", "unidade", "categoria", "quantidade")
    list_filter = ("categoria",)
    search_fields = ("nome",)


@admin.register(Alimentacao)
class AlimentacaoAdmin(admin.ModelAdmin):
    list_display = ("id_alimentacao", "animal", "produto", "data", "quantidade")
    date_hierarchy = "data"


@admin.register(ConsumoSetor)
class ConsumoSetorAdmin(admin.ModelAdmin):
    list_display = ("id_consumo", "setor", "produto", "data", "quantidade")
    date_hierarchy = "data"


class DietaProdutoInline(admin.TabularInline):
    model = DietaProduto
    extra = 1


@admin.register(Dieta)
class DietaAdmin(admin.ModelAdmin):
    list_display = ("nome", "setor")
    inlines = [DietaProdutoInline]