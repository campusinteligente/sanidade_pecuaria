from django.conf import settings
from django.db import models

from animais.models import Animal, Setor


class TipoMedicamento(models.Model):
    id_tipo_medicamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Tipo de Medicamento"
        verbose_name_plural = "Tipos de Medicamento"

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    principio_ativo = models.CharField(max_length=150, blank=True)
    apresentacao = models.CharField(max_length=100, blank=True)
    tipo_medicamento = models.ForeignKey(
        TipoMedicamento, on_delete=models.SET_NULL, null=True, blank=True, related_name="medicamentos"
    )

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class ViaAdministracao(models.Model):
    """RF21 - Vias de administração de medicamentos."""

    id_via = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Via de Administração"
        verbose_name_plural = "Vias de Administração"

    def __str__(self):
        return self.nome


class Diagnostico(models.Model):
    """RF17 - Diagnósticos."""

    id_diagnostico = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class StatusRegistro(models.TextChoices):
    ABERTO = "aberto", "Aberto"
    EM_ANDAMENTO = "em_andamento", "Em andamento"
    CONCLUIDO = "concluido", "Concluído"
    CANCELADO = "cancelado", "Cancelado"


class RegistroSanitario(models.Model):
    """RF16 - Registros sanitários dos animais."""

    id_registro = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="registros_sanitarios")
    data = models.DateField()
    observacao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=StatusRegistro.choices, default=StatusRegistro.ABERTO)

    class Meta:
        verbose_name = "Registro Sanitário"
        verbose_name_plural = "Registros Sanitários"
        ordering = ["-data"]

    def __str__(self):
        return f"Registro #{self.id_registro} - {self.animal}"


class Ocorrencia(models.Model):
    """RF18 - Ocorrências sanitárias."""

    id_ocorrencia = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="ocorrencias")
    diagnostico = models.ForeignKey(
        Diagnostico, on_delete=models.SET_NULL, null=True, blank=True, related_name="ocorrencias"
    )
    data = models.DateField()
    sintomas = models.TextField()
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ocorrência Sanitária"
        verbose_name_plural = "Ocorrências Sanitárias"
        ordering = ["-data"]

    def __str__(self):
        return f"Ocorrência #{self.id_ocorrencia} - {self.animal}"


class PrescricaoVeterinaria(models.Model):
    """RF19 - Prescrições veterinárias."""

    id_prescricao = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="prescricoes")
    data = models.DateField()
    dosagem = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100, blank=True)
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Prescrição Veterinária"
        verbose_name_plural = "Prescrições Veterinárias"
        ordering = ["-data"]

    def __str__(self):
        return f"Prescrição #{self.id_prescricao} - {self.animal}"


class AplicacaoMedicamento(models.Model):
    """RF20 - Aplicações de medicamentos."""

    id_aplicacao = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="aplicacoes")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name="aplicacoes")
    via_aplicacao = models.ForeignKey(
        ViaAdministracao, on_delete=models.SET_NULL, null=True, blank=True, related_name="aplicacoes"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="aplicacoes"
    )
    data = models.DateField()
    dose = models.CharField(max_length=100)
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Aplicação de Medicamento"
        verbose_name_plural = "Aplicações de Medicamentos"
        ordering = ["-data"]

    def __str__(self):
        return f"Aplicação #{self.id_aplicacao} - {self.animal}"


class Vacinacao(models.Model):
    """RF22 - Vacinação."""

    id_vacinacao = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vacinacoes")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name="vacinacoes")
    data = models.DateField()
    dose = models.CharField(max_length=100)
    proxima_dose = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Vacinação"
        verbose_name_plural = "Vacinações"
        ordering = ["-data"]

    def __str__(self):
        return f"Vacinação #{self.id_vacinacao} - {self.animal}"


class Vermifugacao(models.Model):
    """RF23 - Vermifugações."""

    id_vermifugacao = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vermifugacoes")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name="vermifugacoes")
    data = models.DateField()
    dose = models.CharField(max_length=100)
    proxima_aplicacao = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Vermifugação"
        verbose_name_plural = "Vermifugações"
        ordering = ["-data"]

    def __str__(self):
        return f"Vermifugação #{self.id_vermifugacao} - {self.animal}"


class Tratamento(models.Model):
    """RF24 - Tratamentos."""

    id_tratamento = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="tratamentos")
    diagnostico = models.ForeignKey(
        Diagnostico, on_delete=models.SET_NULL, null=True, blank=True, related_name="tratamentos"
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    protocolo = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=StatusRegistro.choices, default=StatusRegistro.EM_ANDAMENTO)

    class Meta:
        verbose_name = "Tratamento"
        verbose_name_plural = "Tratamentos"
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"Tratamento #{self.id_tratamento} - {self.animal}"


class TratamentoMedicamento(models.Model):
    """RF25 - Medicamentos utilizados no tratamento."""

    id_tratamento_medicamento = models.AutoField(primary_key=True)
    tratamento = models.ForeignKey(Tratamento, on_delete=models.CASCADE, related_name="medicamentos_utilizados")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name="tratamentos_utilizados")
    dose = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Medicamento do Tratamento"
        verbose_name_plural = "Medicamentos do Tratamento"

    def __str__(self):
        return f"{self.medicamento} em {self.tratamento}"


class ProtocoloSanitario(models.Model):
    """RF30 - Protocolos sanitários."""

    id_protocolo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    periodicidade = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Protocolo Sanitário"
        verbose_name_plural = "Protocolos Sanitários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class ProtocoloSetor(models.Model):
    """RF31 - Protocolos por setor."""

    id_protocolo_setor = models.AutoField(primary_key=True)
    protocolo = models.ForeignKey(ProtocoloSanitario, on_delete=models.CASCADE, related_name="setores")
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="protocolos")

    class Meta:
        verbose_name = "Protocolo por Setor"
        verbose_name_plural = "Protocolos por Setor"
        unique_together = ("protocolo", "setor")

    def __str__(self):
        return f"{self.protocolo} - {self.setor}"


class HistoricoSanitario(models.Model):
    """RF41 - Histórico sanitário do animal."""

    id_historico = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="historico_sanitario")
    data = models.DateField()
    tipo_evento = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Histórico Sanitário"
        verbose_name_plural = "Históricos Sanitários"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.tipo_evento} - {self.animal}"


class RelatorioSanitario(models.Model):
    """RF44 - Relatórios sanitários."""

    id_relatorio = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    periodo_inicio = models.DateField()
    periodo_fim = models.DateField()
    data_geracao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="relatorios"
    )

    class Meta:
        verbose_name = "Relatório Sanitário"
        verbose_name_plural = "Relatórios Sanitários"
        ordering = ["-data_geracao"]

    def __str__(self):
        return f"Relatório {self.tipo} #{self.id_relatorio}"


class LogAuditoria(models.Model):
    """RF45 - Registros de auditoria."""

    id_log = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs"
    )
    acao = models.CharField(max_length=150)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.acao} ({self.data:%d/%m/%Y})"
