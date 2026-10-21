from django.db import models


class Setor(models.Model):
    class Tipo(models.TextChoices):
        BOVINOCULTURA_CORTE = "bovino_corte", "Bovinocultura de corte"
        BOVINOCULTURA_LEITE = "bovino_leite", "Bovinocultura de leite"
        CAPRINOCULTURA = "caprinocultura", "Caprinocultura"
        AVICULTURA = "avicultura", "Avicultura"
        SUINOCULTURA = "suinocultura", "Suinocultura"

    id_setor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=20, choices=Tipo.choices, verbose_name="Tipo de produção", blank=True
    )
    descricao = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Animal(models.Model):
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        FEMEA = "F", "Fêmea"

    id_animal = models.AutoField(primary_key=True)
    identificacao = models.CharField(max_length=50, unique=True, help_text="Brinco/registro do animal")
    especie = models.CharField(max_length=50, verbose_name="Espécie")
    raca = models.CharField(max_length=50, blank=True, verbose_name="Raça")
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name="animais")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        ordering = ["identificacao"]

    def __str__(self):
        return self.identificacao
