from django.db import models

from animais.models import Animal, Setor


class TipoAlimentacao(models.Model):
    """RF33 - Tipos de alimentação."""

    id_tipo_alimentacao = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tipo de Alimentação"
        verbose_name_plural = "Tipos de Alimentação"

    def __str__(self):
        return self.nome


class ProdutoAlimentar(models.Model):
    """RF34 - Produtos alimentares."""

    id_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    unidade = models.CharField(max_length=20, help_text="Ex.: kg, L, saca")
    categoria = models.CharField(max_length=100, blank=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Estoque atual")

    class Meta:
        verbose_name = "Produto Alimentar"
        verbose_name_plural = "Produtos Alimentares"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Alimentacao(models.Model):
    """RF32 - Alimentação dos animais."""

    id_alimentacao = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="alimentacoes")
    produto = models.ForeignKey(ProdutoAlimentar, on_delete=models.PROTECT, related_name="alimentacoes")
    data = models.DateField()
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Alimentação"
        verbose_name_plural = "Alimentações"
        ordering = ["-data"]

    def __str__(self):
        return f"Alimentação #{self.id_alimentacao} - {self.animal}"


class ConsumoSetor(models.Model):
    """RF36 - Consumo alimentar por setor."""

    id_consumo = models.AutoField(primary_key=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="consumos")
    produto = models.ForeignKey(ProdutoAlimentar, on_delete=models.PROTECT, related_name="consumos")
    data = models.DateField()
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Consumo por Setor"
        verbose_name_plural = "Consumos por Setor"
        ordering = ["-data"]

    def __str__(self):
        return f"Consumo #{self.id_consumo} - {self.setor}"


class Dieta(models.Model):
    """RF37 - Dietas dos animais."""

    id_dieta = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name="dietas")

    class Meta:
        verbose_name = "Dieta"
        verbose_name_plural = "Dietas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class DietaProduto(models.Model):
    """RF38 - Produtos utilizados nas dietas."""

    id_dieta_produto = models.AutoField(primary_key=True)
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, related_name="produtos")
    produto = models.ForeignKey(ProdutoAlimentar, on_delete=models.PROTECT, related_name="dietas")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Produto da Dieta"
        verbose_name_plural = "Produtos da Dieta"
        unique_together = ("dieta", "produto")

    def __str__(self):
        return f"{self.produto} em {self.dieta}"
