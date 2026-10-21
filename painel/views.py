from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from animais.models import Animal, Setor
from sanitario.models import Ocorrencia, RegistroSanitario, Tratamento, Vacinacao
from alimentacao.models import ProdutoAlimentar


@login_required
def dashboard(request):
    context = {
        "active": "dashboard",
        "total_animais": Animal.objects.filter(ativo=True).count(),
        "total_setores": Setor.objects.count(),
        "tratamentos_em_andamento": Tratamento.objects.filter(status="em_andamento").count(),
        "ocorrencias_recentes": Ocorrencia.objects.select_related("animal", "diagnostico").order_by("-data")[:5],
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
