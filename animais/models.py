from django.db import models


class Setor(models.Model):
    id_setor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

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
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True)
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
