from common.crud import CrudConfig, crud_path

from .models import Animal, Setor

setor_cfg = CrudConfig(
    model=Setor,
    url_basename="setor",
    verbose_name="Setor",
    verbose_name_plural="Setores",
    icon="icon-branch",
    list_fields=[("nome", "Nome"), ("get_tipo_display", "Tipo de produção"), ("descricao", "Descrição")],
    search_fields=["nome"],
)

animal_cfg = CrudConfig(
    model=Animal,
    url_basename="animal",
    verbose_name="Animal",
    verbose_name_plural="Animais",
    icon="icon-tag",
    list_fields=[
        ("identificacao", "Identificação"),
        ("especie", "Espécie"),
        ("raca", "Raça"),
        ("sexo", "Sexo"),
        ("setor", "Setor"),
        ("ativo", "Ativo"),
    ],
    search_fields=["identificacao", "especie", "raca"],
    filtrar_por_setor_da_sessao="setor",
)

urlpatterns = [
    crud_path("setores/", setor_cfg),
    crud_path("animais/", animal_cfg),
]
