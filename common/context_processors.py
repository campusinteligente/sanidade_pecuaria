from animais.models import Setor


def setor_atual(request):
    """Disponibiliza em todos os templates:
    - setores_disponiveis: todos os setores cadastrados (pro seletor da sidebar)
    - setor_atual: o setor escolhido na sessão (ou None = "todos os setores")
    """
    if not request.user.is_authenticated:
        return {}

    setor_id = request.session.get("setor_id")
    setor = None
    if setor_id:
        setor = Setor.objects.filter(pk=setor_id).first()

    return {
        "setores_disponiveis": Setor.objects.all(),
        "setor_atual": setor,
    }
