from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Animal, PerfilUsuario, Setor


class SimpleUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário simplificado para o admin.
    Senha padrão pré-preenchida como 'ifsuldeminas'; sem validações complexas."""

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "ifsuldeminas"}),
        initial="ifsuldeminas",
        help_text="Senha padrão: <strong>ifsuldeminas</strong>. Pode ser alterada após o cadastro.",
        required=True,
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={"placeholder": "ifsuldeminas"}),
        initial="ifsuldeminas",
        help_text="Repita a senha.",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        help_texts = {
            "username": "Padrão: <strong>nome.sobrenome</strong> (ex: joao.silva). "
                        "Somente letras, números, ponto, hífen e sublinhado.",
        }

    def _post_clean(self):
        # Pula a validação de força de senha do formulário base.
        super(UserCreationForm, self)._post_clean()

    def validate_passwords(self):
        pass


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name = "Setor do usuário"
    verbose_name_plural = "Setor vinculado ao usuário"


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = SimpleUserCreationForm
    inlines = (PerfilUsuarioInline,)
    list_display = ("username", "email", "get_setor", "is_staff", "is_superuser")

    # Campos exibidos na tela de CRIAÇÃO — só o essencial
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2"),
        }),
    )

    @admin.display(description="Setor vinculado")
    def get_setor(self, obj):
        return obj.perfil.setor.nome if hasattr(obj, "perfil") and obj.perfil.setor else "Todos os setores (Geral)"


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "setor")
    list_filter = ("setor",)
    search_fields = ("user__username", "setor__nome")


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "descricao")
    list_filter = ("tipo",)
    search_fields = ("nome",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("identificacao", "especie", "raca", "sexo", "setor", "ativo")
    list_filter = ("especie", "sexo", "ativo", "setor")
    search_fields = ("identificacao", "raca")

