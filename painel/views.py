from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from animais.models import Animal, Setor
from sanitario.models import Ocorrencia, RegistroSanitario, Tratamento, Vacinacao
from alimentacao.models import ProdutoAlimentar


@login_required
def dashboard(request):
    setor_id = None
    if hasattr(request.user, "perfil") and request.user.perfil.setor_id:
        setor_id = request.user.perfil.setor_id
    else:
        setor_id = request.session.get("setor_id")

    animais_qs = Animal.objects.filter(ativo=True)
    tratamentos_qs = Tratamento.objects.filter(status="em_andamento")
    ocorrencias_qs = Ocorrencia.objects.all()

    if setor_id:
        animais_qs = animais_qs.filter(setor_id=setor_id)
        tratamentos_qs = tratamentos_qs.filter(animal__setor_id=setor_id)
        ocorrencias_qs = ocorrencias_qs.filter(animal__setor_id=setor_id)

    context = {
        "active": "dashboard",
        "total_animais": animais_qs.count(),
        "total_setores": Setor.objects.count(),
        "tratamentos_em_andamento": tratamentos_qs.count(),
        "total_ocorrencias": ocorrencias_qs.count(),
        "modulos": [
            {
                "titulo": "Registros sanitários",
                "descricao": "Histórico de saúde por animal",
                "icone": "icon-clipboard-pulse",
                "url": reverse('registro_sanitario:listar'),
            },
            {
                "titulo": "Ocorrências",
                "descricao": "Sintomas e diagnósticos registrados",
                "icone": "icon-alert",
                "url": reverse('ocorrencia:listar'),
            },
            {
                "titulo": "Prescrições veterinárias",
                "descricao": "Dosagem, frequência e duração",
                "icone": "icon-file-plus",
                "url": reverse('prescricao:listar'),
            },
            {
                "titulo": "Vacinação",
                "descricao": "Doses aplicadas e próxima dose",
                "icone": "icon-droplet",
                "url": reverse('vacinacao:listar'),
            },
            {
                "titulo": "Vermifugação",
                "descricao": "Controle de aplicações e retorno",
                "icone": "icon-target",
                "url": reverse('vermifugacao:listar'),
            },
            {
                "titulo": "Tratamentos",
                "descricao": "Protocolos e medicamentos utilizados",
                "icone": "icon-heart-pulse",
                "url": reverse('tratamento:listar'),
            },
            {
                "titulo": "Alimentação",
                "descricao": "Consumo diário por animal e setor",
                "icone": "icon-utensils",
                "url": reverse('alimentacao_registro:listar'),
            },
            {
                "titulo": "Dietas",
                "descricao": "Composição de dietas por setor",
                "icone": "icon-clipboard-list",
                "url": reverse('dieta:listar'),
            },
            {
                "titulo": "Relatórios",
                "descricao": "Geração de relatórios sanitários",
                "icone": "icon-bar-chart",
                "url": reverse('relatorio:listar'),
            },
        ],
    }
    return render(request, "painel/dashboard.html", context)


@login_required
def ocorrencias_recentes(request):
    setor_id = None
    if hasattr(request.user, "perfil") and request.user.perfil.setor_id:
        setor_id = request.user.perfil.setor_id
    else:
        setor_id = request.session.get("setor_id")

    qs = Ocorrencia.objects.select_related("animal", "animal__setor", "diagnostico").order_by("-data", "-id_ocorrencia")

    if setor_id:
        qs = qs.filter(animal__setor_id=setor_id)

    termo = request.GET.get("q", "").strip()
    if termo:
        qs = qs.filter(
            Q(animal__identificacao__icontains=termo)
            | Q(sintomas__icontains=termo)
            | Q(observacao__icontains=termo)
            | Q(diagnostico__nome__icontains=termo)
        )

    total_ocorrencias = qs.count()
    com_diagnostico = qs.filter(diagnostico__isnull=False).count()
    sem_diagnostico = total_ocorrencias - com_diagnostico
    animais_afetados = qs.values("animal_id").distinct().count()

    paginator = Paginator(qs, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "active": "ocorrencias_recentes",
        "page_obj": page_obj,
        "objetos": page_obj.object_list,
        "is_paginated": page_obj.has_other_pages(),
        "total_ocorrencias": total_ocorrencias,
        "com_diagnostico": com_diagnostico,
        "sem_diagnostico": sem_diagnostico,
        "animais_afetados": animais_afetados,
        "termo_busca": termo,
    }
    return render(request, "painel/ocorrencias_recentes.html", context)

