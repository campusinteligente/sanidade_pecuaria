from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def definir_setor(request):
    """Guarda na sessão qual setor está 'ativo' — usado pela sidebar para
    filtrar os módulos que têm relação com Setor (Animais, Dietas, etc.).
    Um POST com setor_id vazio limpa o filtro (mostra todos os setores).
    """
    if request.method == "POST":
        setor_id = request.POST.get("setor_id", "").strip()
        if setor_id:
            request.session["setor_id"] = setor_id
        else:
            request.session.pop("setor_id", None)

    proximo = request.META.get("HTTP_REFERER") or "/"
    return redirect(proximo)