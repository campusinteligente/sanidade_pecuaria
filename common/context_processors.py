from animais.models import Setor


def setor_atual(request):
    """Disponibiliza em todos os templates:
    - setores_disponiveis: todos os setores cadastrados (pro seletor da sidebar)
    - setor_atual: o setor escolhido na sessão ou vinculado ao perfil
    - setor_fixo: booleano indicando se o usuário possui setor fixo vinculado ao perfil
    """
    if not request.user.is_authenticated:
        return {}

    user = request.user
    setor_fixo = False
    setor = None

    # Se o usuário possui setor vinculado em seu perfil de cadastro, ele é fixo e exclusivo
    if hasattr(user, "perfil") and user.perfil.setor:
        setor = user.perfil.setor
        setor_fixo = True
        request.session["setor_id"] = str(setor.pk)
    else:
        setor_id = request.session.get("setor_id")
        if setor_id:
            setor = Setor.objects.filter(pk=setor_id).first()

    return {
        "setores_disponiveis": Setor.objects.all().order_by("nome"),
        "setor_atual": setor,
        "setor_fixo": setor_fixo,
    }