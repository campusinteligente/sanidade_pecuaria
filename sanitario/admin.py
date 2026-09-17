from django.contrib import admin

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


@admin.register(TipoMedicamento)
class TipoMedicamentoAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "principio_ativo", "apresentacao", "tipo_medicamento")
    search_fields = ("nome", "principio_ativo")


@admin.register(ViaAdministracao)
class ViaAdministracaoAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(RegistroSanitario)
class RegistroSanitarioAdmin(admin.ModelAdmin):
    list_display = ("id_registro", "animal", "data", "status")
    list_filter = ("status",)
    date_hierarchy = "data"


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ("id_ocorrencia", "animal", "diagnostico", "data")
    date_hierarchy = "data"


@admin.register(PrescricaoVeterinaria)
class PrescricaoVeterinariaAdmin(admin.ModelAdmin):
    list_display = ("id_prescricao", "animal", "data", "dosagem", "frequencia")
    date_hierarchy = "data"


@admin.register(AplicacaoMedicamento)
class AplicacaoMedicamentoAdmin(admin.ModelAdmin):
    list_display = ("id_aplicacao", "animal", "medicamento", "data", "usuario")
    date_hierarchy = "data"


@admin.register(Vacinacao)
class VacinacaoAdmin(admin.ModelAdmin):
    list_display = ("id_vacinacao", "animal", "medicamento", "data", "proxima_dose")
    date_hierarchy = "data"


@admin.register(Vermifugacao)
class VermifugacaoAdmin(admin.ModelAdmin):
    list_display = ("id_vermifugacao", "animal", "medicamento", "data", "proxima_aplicacao")
    date_hierarchy = "data"


class TratamentoMedicamentoInline(admin.TabularInline):
    model = TratamentoMedicamento
    extra = 1


@admin.register(Tratamento)
class TratamentoAdmin(admin.ModelAdmin):
    list_display = ("id_tratamento", "animal", "diagnostico", "data_inicio", "data_fim", "status")
    list_filter = ("status",)
    inlines = [TratamentoMedicamentoInline]


@admin.register(ProtocoloSanitario)
class ProtocoloSanitarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "periodicidade")


@admin.register(ProtocoloSetor)
class ProtocoloSetorAdmin(admin.ModelAdmin):
    list_display = ("protocolo", "setor")


@admin.register(HistoricoSanitario)
class HistoricoSanitarioAdmin(admin.ModelAdmin):
    list_display = ("animal", "tipo_evento", "data")
    date_hierarchy = "data"


@admin.register(RelatorioSanitario)
class RelatorioSanitarioAdmin(admin.ModelAdmin):
    list_display = ("id_relatorio", "tipo", "periodo_inicio", "periodo_fim", "data_geracao", "usuario")


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ("acao", "usuario", "data")
    date_hierarchy = "data"
