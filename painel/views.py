from django.shortcuts import render

from animais.models import Animal, Setor
from sanitario.models import Ocorrencia, RegistroSanitario, Tratamento, Vacinacao
from alimentacao.models import ProdutoAlimentar


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
                "url": "/admin/sanitario/registrosanitario/",
            },
            {
                "titulo": "Ocorrências",
                "descricao": "Sintomas e diagnósticos registrados",
                "icone": "icon-alert",
                "url": "/admin/sanitario/ocorrencia/",
            },
            {
                "titulo": "Prescrições veterinárias",
                "descricao": "Dosagem, frequência e duração",
                "icone": "icon-file-plus",
                "url": "/admin/sanitario/prescricaoveterinaria/",
            },
            {
                "titulo": "Vacinação",
                "descricao": "Doses aplicadas e próxima dose",
                "icone": "icon-droplet",
                "url": "/admin/sanitario/vacinacao/",
            },
            {
                "titulo": "Vermifugação",
                "descricao": "Controle de aplicações e retorno",
                "icone": "icon-target",
                "url": "/admin/sanitario/vermifugacao/",
            },
            {
                "titulo": "Tratamentos",
                "descricao": "Protocolos e medicamentos utilizados",
                "icone": "icon-heart-pulse",
                "url": "/admin/sanitario/tratamento/",
            },
            {
                "titulo": "Alimentação",
                "descricao": "Consumo diário por animal e setor",
                "icone": "icon-utensils",
                "url": "/admin/alimentacao/alimentacao/",
            },
            {
                "titulo": "Dietas",
                "descricao": "Composição de dietas por setor",
                "icone": "icon-clipboard-list",
                "url": "/admin/alimentacao/dieta/",
            },
            {
                "titulo": "Relatórios",
                "descricao": "Geração de relatórios sanitários",
                "icone": "icon-bar-chart",
                "url": "/admin/sanitario/relatoriosanitario/",
            },
        ],
    }
    return render(request, "painel/dashboard.html", context)
