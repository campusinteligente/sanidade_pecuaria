from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from animais.models import Setor


class SetorLoginView(LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["setores"] = Setor.objects.all().order_by("nome")
        return ctx

    def form_valid(self, form):
        user = form.get_user()

        setor_login = self.request.POST.get("setor_login", "").strip()

        # Usuário com setor fixo no perfil
        if hasattr(user, "perfil") and user.perfil.setor_id:
            setor_fixo_id = str(user.perfil.setor_id)

            # Tentou selecionar um setor diferente do seu → barra o acesso
            if setor_login and setor_login != setor_fixo_id:
                from animais.models import Setor as SetorModel
                try:
                    setor_tentado = SetorModel.objects.get(pk=setor_login)
                    nome_tentado = setor_tentado.nome
                except SetorModel.DoesNotExist:
                    nome_tentado = "desconhecido"

                form.add_error(
                    None,
                    f'Seu usuário não está cadastrado no setor "{nome_tentado}". '
                    f'Você só pode acessar o setor "{user.perfil.setor.nome}".',
                )
                return self.form_invalid(form)

            # Setor correto ou sem seleção → vincula o setor fixo
            auth_login(self.request, user)
            self.request.session["setor_id"] = setor_fixo_id

        else:
            # Usuário geral/administrador → pode escolher qualquer setor
            auth_login(self.request, user)
            if setor_login:
                self.request.session["setor_id"] = setor_login
            else:
                self.request.session.pop("setor_id", None)

        return redirect(self.get_success_url())


@login_required
def definir_setor(request):
    """Guarda na sessão qual setor está 'ativo' — usado pela sidebar para
    filtrar os módulos que têm relação com Setor (Animais, Dietas, etc.).
    Se o usuário tem um setor vinculado ao perfil, não permite alterar.
    """
    if hasattr(request.user, "perfil") and request.user.perfil.setor_id:
        request.session["setor_id"] = str(request.user.perfil.setor_id)
        proximo = request.META.get("HTTP_REFERER") or "/"
        return redirect(proximo)

    if request.method == "POST":
        setor_id = request.POST.get("setor_id", "").strip()
        if setor_id:
            request.session["setor_id"] = setor_id
        else:
            request.session.pop("setor_id", None)

    proximo = request.META.get("HTTP_REFERER") or "/"
    return redirect(proximo)

