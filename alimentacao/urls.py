from common.crud import CrudConfig, crud_path

from .models import (
    Alimentacao,
    ConsumoSetor,
    Dieta,
    DietaProduto,
    ProdutoAlimentar,
    TipoAlimentacao,
)

tipo_alimentacao_cfg = CrudConfig(
    model=TipoAlimentacao,
    url_basename="tipo_alimentacao",
    verbose_name="Tipo de Alimentação",
    verbose_name_plural="Tipos de Alimentação",
    icon="icon-utensils",
    list_fields=[("nome", "Nome"), ("descricao", "Descrição")],
    search_fields=["nome"],
)

produto_cfg = CrudConfig(
    model=ProdutoAlimentar,
    url_basename="produto",
    verbose_name="Produto Alimentar",
    verbose_name_plural="Produtos Alimentares",
    icon="icon-basket",
    list_fields=[
        ("nome", "Nome"),
        ("unidade", "Unidade"),
        ("categoria", "Categoria"),
        ("quantidade", "Estoque"),
    ],
    search_fields=["nome", "categoria"],
)

alimentacao_cfg = CrudConfig(
    model=Alimentacao,
    url_basename="alimentacao_registro",
    verbose_name="Alimentação",
    verbose_name_plural="Alimentações",
    icon="icon-utensils",
    list_fields=[
        ("animal", "Animal"),
        ("produto", "Produto"),
        ("data", "Data"),
        ("quantidade", "Quantidade"),
    ],
)

consumo_setor_cfg = CrudConfig(
    model=ConsumoSetor,
    url_basename="consumo_setor",
    verbose_name="Consumo por Setor",
    verbose_name_plural="Consumos por Setor",
    icon="icon-basket",
    list_fields=[
        ("setor", "Setor"),
        ("produto", "Produto"),
        ("data", "Data"),
        ("quantidade", "Quantidade"),
    ],
)

dieta_cfg = CrudConfig(
    model=Dieta,
    url_basename="dieta",
    verbose_name="Dieta",
    verbose_name_plural="Dietas",
    icon="icon-clipboard-list",
    list_fields=[("nome", "Nome"), ("setor", "Setor")],
    search_fields=["nome"],
)

dieta_produto_cfg = CrudConfig(
    model=DietaProduto,
    url_basename="dieta_produto",
    verbose_name="Produto da Dieta",
    verbose_name_plural="Produtos da Dieta",
    icon="icon-clipboard-list",
    list_fields=[("dieta", "Dieta"), ("produto", "Produto"), ("quantidade", "Quantidade")],
)

urlpatterns = [
    crud_path("tipos-alimentacao/", tipo_alimentacao_cfg),
    crud_path("produtos/", produto_cfg),
    crud_path("alimentacoes/", alimentacao_cfg),
    crud_path("consumos-setor/", consumo_setor_cfg),
    crud_path("dietas/", dieta_cfg),
    crud_path("dietas-produtos/", dieta_produto_cfg),
]