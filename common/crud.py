"""
CRUD genérico.

Em vez de escrever ListView/CreateView/UpdateView/DeleteView na mão para
cada um dos ~25 models do projeto, descrevemos cada módulo com um
`CrudConfig` e a função `build_crud_urls` monta as 4 views + as URLs
(listar, criar, editar, apagar), todas usando os mesmos 3 templates em
templates/common/.
"""
from dataclasses import dataclass, field

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import ChoiceField, ModelChoiceField
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


def _traduzir_campos_selecao(form):
    """O Django 6.1 usa por padrão o texto em inglês '- Select an option -'
    nos campos de seleção (chave estrangeira e CharField com choices), e
    essa string ainda não tem tradução pt-br no pacote. Trocamos aqui para
    não aparecer em inglês no formulário.
    """
    for campo in form.fields.values():
        if isinstance(campo, ModelChoiceField):
            campo.empty_label = "Selecione..."
        elif isinstance(campo, ChoiceField):
            campo.choices = [
                (valor, "Selecione...") if valor == "" else (valor, rotulo)
                for valor, rotulo in campo.choices
            ]
    return form


@dataclass
class CrudConfig:
    model: object
    url_basename: str            # usado como namespace da URL, ex: "animal"
    verbose_name: str            # "Animal"
    verbose_name_plural: str     # "Animais"
    icon: str = "icon-grid"      # id do símbolo em templates/_icons.html
    list_fields: list = field(default_factory=list)   # [("campo", "Rótulo"), ...]
    form_fields: object = "__all__"
    search_fields: list = field(default_factory=list)
    paginate_by: int = 15
    filtrar_por_setor_da_sessao: str = ""   # nome do campo FK pra Setor, ex: "setor"


def build_crud_urls(config: CrudConfig):
    """Retorna a lista de urlpatterns (listar/novo/editar/apagar) para o model."""

    list_url_name = f"{config.url_basename}:listar"

    class GenericListView(LoginRequiredMixin, ListView):
        model = config.model
        template_name = "common/crud_list.html"
        context_object_name = "objetos"
        paginate_by = config.paginate_by

        def get_queryset(self):
            qs = super().get_queryset()
            termo = self.request.GET.get("q", "").strip()
            if termo and config.search_fields:
                condicao = Q()
                for campo in config.search_fields:
                    condicao |= Q(**{f"{campo}__icontains": termo})
                qs = qs.filter(condicao)

            setor_id = None
            if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                setor_id = self.request.user.perfil.setor_id
            else:
                setor_id = self.request.session.get("setor_id")

            if setor_id:
                campo_setor = config.filtrar_por_setor_da_sessao
                if not campo_setor:
                    field_names = [f.name for f in config.model._meta.get_fields()]
                    if "setor" in field_names:
                        campo_setor = "setor"
                    elif "animal" in field_names:
                        campo_setor = "animal__setor"
                    elif "dieta" in field_names:
                        campo_setor = "dieta__setor"
                    elif "tratamento" in field_names:
                        campo_setor = "tratamento__animal__setor"

                if campo_setor:
                    try:
                        qs = qs.filter(**{f"{campo_setor}_id": setor_id})
                    except Exception:
                        pass
            return qs

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            respeita_filtro = bool(config.filtrar_por_setor_da_sessao)
            if not respeita_filtro:
                field_names = [f.name for f in config.model._meta.get_fields()]
                respeita_filtro = any(f in field_names for f in ("setor", "animal", "dieta", "tratamento"))

            ctx.update(
                titulo=config.verbose_name_plural,
                icone=config.icon,
                list_fields=config.list_fields,
                url_basename=config.url_basename,
                termo_busca=self.request.GET.get("q", ""),
                respeita_filtro_setor=respeita_filtro,
            )
            return ctx

    class GenericCreateView(LoginRequiredMixin, CreateView):
        model = config.model
        fields = config.form_fields
        template_name = "common/crud_form.html"
        success_url = reverse_lazy(list_url_name)

        def get_form(self, form_class=None):
            form = _traduzir_campos_selecao(super().get_form(form_class))
            setor_id = None
            if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                setor_id = self.request.user.perfil.setor_id
            else:
                setor_id = self.request.session.get("setor_id")

            if setor_id:
                if "setor" in form.fields:
                    form.fields["setor"].initial = setor_id
                    if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                        from animais.models import Setor
                        form.fields["setor"].queryset = Setor.objects.filter(pk=setor_id)
                        form.fields["setor"].empty_label = None

                if "animal" in form.fields:
                    from animais.models import Animal
                    form.fields["animal"].queryset = Animal.objects.filter(setor_id=setor_id, ativo=True)

                if "dieta" in form.fields:
                    from alimentacao.models import Dieta
                    form.fields["dieta"].queryset = Dieta.objects.filter(setor_id=setor_id)

                if "tratamento" in form.fields:
                    from sanitario.models import Tratamento
                    form.fields["tratamento"].queryset = Tratamento.objects.filter(animal__setor_id=setor_id)

            return form

        def form_valid(self, form):
            setor_id = None
            if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                setor_id = self.request.user.perfil.setor_id
            else:
                setor_id = self.request.session.get("setor_id")

            if setor_id and hasattr(form.instance, "setor_id") and not form.instance.setor_id:
                try:
                    form.instance.setor_id = int(setor_id)
                except (ValueError, TypeError):
                    pass
            return super().form_valid(form)

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(
                titulo=f"Novo(a) {config.verbose_name}",
                icone=config.icon,
                url_basename=config.url_basename,
            )
            return ctx

    class GenericUpdateView(LoginRequiredMixin, UpdateView):
        model = config.model
        fields = config.form_fields
        template_name = "common/crud_form.html"
        success_url = reverse_lazy(list_url_name)

        def get_form(self, form_class=None):
            form = _traduzir_campos_selecao(super().get_form(form_class))
            setor_id = None
            if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                setor_id = self.request.user.perfil.setor_id
            else:
                setor_id = self.request.session.get("setor_id")

            if setor_id:
                if "setor" in form.fields:
                    if hasattr(self.request.user, "perfil") and self.request.user.perfil.setor_id:
                        from animais.models import Setor
                        form.fields["setor"].queryset = Setor.objects.filter(pk=setor_id)
                        form.fields["setor"].empty_label = None

                if "animal" in form.fields:
                    from animais.models import Animal
                    form.fields["animal"].queryset = Animal.objects.filter(setor_id=setor_id)

                if "dieta" in form.fields:
                    from alimentacao.models import Dieta
                    form.fields["dieta"].queryset = Dieta.objects.filter(setor_id=setor_id)

                if "tratamento" in form.fields:
                    from sanitario.models import Tratamento
                    form.fields["tratamento"].queryset = Tratamento.objects.filter(animal__setor_id=setor_id)

            return form

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(
                titulo=f"Editar {config.verbose_name}",
                icone=config.icon,
                url_basename=config.url_basename,
            )
            return ctx

    class GenericDeleteView(LoginRequiredMixin, DeleteView):
        model = config.model
        template_name = "common/crud_confirm_delete.html"
        success_url = reverse_lazy(list_url_name)

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(titulo=config.verbose_name, url_basename=config.url_basename)
            return ctx

    return [
        path("", GenericListView.as_view(), name="listar"),
        path("novo/", GenericCreateView.as_view(), name="criar"),
        path("<int:pk>/editar/", GenericUpdateView.as_view(), name="editar"),
        path("<int:pk>/apagar/", GenericDeleteView.as_view(), name="apagar"),
    ]


def crud_path(url_prefix, config: CrudConfig):
    """Atalho: path(prefixo, include(CRUD do model, namespace=config.url_basename))."""
    urls = build_crud_urls(config)
    return path(url_prefix, include((urls, config.url_basename), namespace=config.url_basename))
