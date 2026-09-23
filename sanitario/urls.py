from common.crud import CrudConfig, crud_path

from .models import (
    AplicacaoMedicamento,
    Diagnostico,
    HistoricoSanitario,
    LogAuditoria,
    Medicamento,
    Ocorrencia,
    PrescricaoVeterinaria,
    ProtocoloSanitario,
    ProtocoloSetor,
    RegistroSanitario,
    RelatorioSanitario,
    Tratamento,
    TratamentoMedicamento,
    TipoMedicamento,
    Vacinacao,
    ViaAdministracao,
    Vermifugacao,
)

tipo_medicamento_cfg = CrudConfig(
    model=TipoMedicamento,
    url_basename="tipo_medicamento",
    verbose_name="Tipo de Medicamento",
    verbose_name_plural="Tipos de Medicamento",
    icon="icon-check-square",
    list_fields=[("nome", "Nome")],
    search_fields=["nome"],
)

medicamento_cfg = CrudConfig(
    model=Medicamento,
    url_basename="medicamento",
    verbose_name="Medicamento",
    verbose_name_plural="Medicamentos",
    icon="icon-droplet",
    list_fields=[
        ("nome", "Nome"),
        ("principio_ativo", "Princípio ativo"),
        ("apresentacao", "Apresentação"),
        ("tipo_medicamento", "Tipo"),
    ],
    search_fields=["nome", "principio_ativo"],
)

via_administracao_cfg = CrudConfig(
    model=ViaAdministracao,
    url_basename="via_administracao",
    verbose_name="Via de Administração",
    verbose_name_plural="Vias de Administração",
    icon="icon-target",
    list_fields=[("nome", "Nome"), ("descricao", "Descrição")],
    search_fields=["nome"],
)

diagnostico_cfg = CrudConfig(
    model=Diagnostico,
    url_basename="diagnostico",
    verbose_name="Diagnóstico",
    verbose_name_plural="Diagnósticos",
    icon="icon-clipboard-pulse",
    list_fields=[("nome", "Nome"), ("descricao", "Descrição")],
    search_fields=["nome"],
)

registro_sanitario_cfg = CrudConfig(
    model=RegistroSanitario,
    url_basename="registro_sanitario",
    verbose_name="Registro Sanitário",
    verbose_name_plural="Registros Sanitários",
    icon="icon-clipboard-pulse",
    list_fields=[("animal", "Animal"), ("data", "Data"), ("status", "Status")],
    search_fields=["observacao"],
)

ocorrencia_cfg = CrudConfig(
    model=Ocorrencia,
    url_basename="ocorrencia",
    verbose_name="Ocorrência",
    verbose_name_plural="Ocorrências",
    icon="icon-alert",
    list_fields=[
        ("animal", "Animal"),
        ("diagnostico", "Diagnóstico"),
        ("data", "Data"),
        ("sintomas", "Sintomas"),
    ],
    search_fields=["sintomas", "observacao"],
)

prescricao_cfg = CrudConfig(
    model=PrescricaoVeterinaria,
    url_basename="prescricao",
    verbose_name="Prescrição Veterinária",
    verbose_name_plural="Prescrições Veterinárias",
    icon="icon-file-plus",
    list_fields=[
        ("animal", "Animal"),
        ("data", "Data"),
        ("dosagem", "Dosagem"),
        ("frequencia", "Frequência"),
    ],
    search_fields=["dosagem", "frequencia"],
)

aplicacao_cfg = CrudConfig(
    model=AplicacaoMedicamento,
    url_basename="aplicacao",
    verbose_name="Aplicação de Medicamento",
    verbose_name_plural="Aplicações de Medicamentos",
    icon="icon-droplet",
    list_fields=[
        ("animal", "Animal"),
        ("medicamento", "Medicamento"),
        ("via_aplicacao", "Via"),
        ("data", "Data"),
        ("usuario", "Usuário"),
    ],
)

vacinacao_cfg = CrudConfig(
    model=Vacinacao,
    url_basename="vacinacao",
    verbose_name="Vacinação",
    verbose_name_plural="Vacinações",
    icon="icon-droplet",
    list_fields=[
        ("animal", "Animal"),
        ("medicamento", "Medicamento"),
        ("data", "Data"),
        ("proxima_dose", "Próxima dose"),
    ],
)

vermifugacao_cfg = CrudConfig(
    model=Vermifugacao,
    url_basename="vermifugacao",
    verbose_name="Vermifugação",
    verbose_name_plural="Vermifugações",
    icon="icon-target",
    list_fields=[
        ("animal", "Animal"),
        ("medicamento", "Medicamento"),
        ("data", "Data"),
        ("proxima_aplicacao", "Próxima aplicação"),
    ],
)

tratamento_cfg = CrudConfig(
    model=Tratamento,
    url_basename="tratamento",
    verbose_name="Tratamento",
    verbose_name_plural="Tratamentos",
    icon="icon-heart-pulse",
    list_fields=[
        ("animal", "Animal"),
        ("diagnostico", "Diagnóstico"),
        ("data_inicio", "Início"),
        ("data_fim", "Fim"),
        ("status", "Status"),
    ],
)

tratamento_medicamento_cfg = CrudConfig(
    model=TratamentoMedicamento,
    url_basename="tratamento_medicamento",
    verbose_name="Medicamento do Tratamento",
    verbose_name_plural="Medicamentos do Tratamento",
    icon="icon-heart-pulse",
    list_fields=[
        ("tratamento", "Tratamento"),
        ("medicamento", "Medicamento"),
        ("dose", "Dose"),
        ("frequencia", "Frequência"),
    ],
)

protocolo_cfg = CrudConfig(
    model=ProtocoloSanitario,
    url_basename="protocolo",
    verbose_name="Protocolo Sanitário",
    verbose_name_plural="Protocolos Sanitários",
    icon="icon-check-square",
    list_fields=[("nome", "Nome"), ("periodicidade", "Periodicidade")],
    search_fields=["nome"],
)

protocolo_setor_cfg = CrudConfig(
    model=ProtocoloSetor,
    url_basename="protocolo_setor",
    verbose_name="Protocolo por Setor",
    verbose_name_plural="Protocolos por Setor",
    icon="icon-check-square",
    list_fields=[("protocolo", "Protocolo"), ("setor", "Setor")],
    filtrar_por_setor_da_sessao="setor",
)

historico_cfg = CrudConfig(
    model=HistoricoSanitario,
    url_basename="historico",
    verbose_name="Histórico Sanitário",
    verbose_name_plural="Histórico Sanitário",
    icon="icon-clock",
    list_fields=[
        ("animal", "Animal"),
        ("tipo_evento", "Tipo de evento"),
        ("data", "Data"),
    ],
)

relatorio_cfg = CrudConfig(
    model=RelatorioSanitario,
    url_basename="relatorio",
    verbose_name="Relatório Sanitário",
    verbose_name_plural="Relatórios Sanitários",
    icon="icon-bar-chart",
    list_fields=[
        ("tipo", "Tipo"),
        ("periodo_inicio", "Início do período"),
        ("periodo_fim", "Fim do período"),
        ("usuario", "Usuário"),
    ],
)

log_auditoria_cfg = CrudConfig(
    model=LogAuditoria,
    url_basename="log_auditoria",
    verbose_name="Log de Auditoria",
    verbose_name_plural="Logs de Auditoria",
    icon="icon-list",
    list_fields=[("acao", "Ação"), ("usuario", "Usuário"), ("data", "Data")],
    search_fields=["acao"],
)

urlpatterns = [
    crud_path("tipos-medicamento/", tipo_medicamento_cfg),
    crud_path("medicamentos/", medicamento_cfg),
    crud_path("vias-administracao/", via_administracao_cfg),
    crud_path("diagnosticos/", diagnostico_cfg),
    crud_path("registros-sanitarios/", registro_sanitario_cfg),
    crud_path("ocorrencias/", ocorrencia_cfg),
    crud_path("prescricoes/", prescricao_cfg),
    crud_path("aplicacoes/", aplicacao_cfg),
    crud_path("vacinacoes/", vacinacao_cfg),
    crud_path("vermifugacoes/", vermifugacao_cfg),
    crud_path("tratamentos/", tratamento_cfg),
    crud_path("tratamentos-medicamentos/", tratamento_medicamento_cfg),
    crud_path("protocolos/", protocolo_cfg),
    crud_path("protocolos-setor/", protocolo_setor_cfg),
    crud_path("historico-sanitario/", historico_cfg),
    crud_path("relatorios/", relatorio_cfg),
    crud_path("auditoria/", log_auditoria_cfg),
]
