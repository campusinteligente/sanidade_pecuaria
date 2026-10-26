import io
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from alimentacao.models import ConsumoSetor, Dieta, ProdutoAlimentar
from animais.models import Animal, Setor
from sanitario.models import (
    LogAuditoria,
    Ocorrencia,
    RegistroSanitario,
    RelatorioSanitario,
    Tratamento,
    Vacinacao,
    Vermifugacao,
)


class NumberedCanvas(canvas.Canvas):
    """Adiciona numeração 'Página X de Y' e cabeçalho/rodapé padronizados a cada página."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        width, height = self._pagesize

        # Rodapé com linha e numeração
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(1.5 * cm, 1.2 * cm, width - 1.5 * cm, 1.2 * cm)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(
            1.5 * cm,
            0.8 * cm,
            "Campus Inteligente — Sistema de Gestão Sanitária e Alimentar da Pecuária",
        )
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(width - 1.5 * cm, 0.8 * cm, page_str)

        self.restoreState()


def formatar_data(val):
    if not val:
        return "—"
    if isinstance(val, (date, datetime)):
        return val.strftime("%d/%m/%Y")
    return str(val)


def coletar_dados_relatorio(tipo, data_inicio, data_fim, setor_id):
    """Retorna titulo, colunas, lista de linhas (tuplas) e kpis para o tipo escolhido."""

    if tipo == "ocorrencias":
        titulo = "Relatório de Ocorrências Sanitárias"
        colunas = ["Data", "Animal", "Setor", "Diagnóstico", "Sintomas", "Observações"]
        qs = Ocorrencia.objects.select_related("animal", "animal__setor", "diagnostico").order_by(
            "-data", "-id_ocorrencia"
        )
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        if setor_id:
            qs = qs.filter(animal__setor_id=setor_id)

        linhas = []
        for o in qs:
            animal_str = str(o.animal)
            setor_str = o.animal.setor.nome if (o.animal and o.animal.setor) else "—"
            diag_str = o.diagnostico.nome if o.diagnostico else "Em avaliação"
            linhas.append(
                [
                    formatar_data(o.data),
                    animal_str,
                    setor_str,
                    diag_str,
                    o.sintomas or "—",
                    o.observacao or "—",
                ]
            )

        kpis = [
            ("Total de ocorrências", len(linhas)),
            ("Com diagnóstico", qs.filter(diagnostico__isnull=False).count()),
            ("Em avaliação", qs.filter(diagnostico__isnull=True).count()),
        ]

    elif tipo == "animais":
        titulo = "Relatório de Rebanho e Animais Cadastrados"
        colunas = ["Identificação", "Espécie", "Raça", "Sexo", "Setor", "Data Nasc.", "Situação"]
        qs = Animal.objects.select_related("setor").order_by("identificacao")
        if setor_id:
            qs = qs.filter(setor_id=setor_id)

        linhas = []
        for a in qs:
            setor_str = a.setor.nome if a.setor else "—"
            linhas.append(
                [
                    a.identificacao,
                    a.especie or "—",
                    a.raca or "—",
                    a.get_sexo_display() if hasattr(a, "get_sexo_display") else a.sexo,
                    setor_str,
                    formatar_data(a.data_nascimento),
                    "Ativo" if a.ativo else "Inativo",
                ]
            )

        kpis = [
            ("Total de animais", len(linhas)),
            ("Animais ativos", qs.filter(ativo=True).count()),
            ("Fêmeas", qs.filter(sexo="F").count()),
            ("Machos", qs.filter(sexo="M").count()),
        ]

    elif tipo == "tratamentos":
        titulo = "Relatório de Tratamentos Veterinários"
        colunas = ["Início", "Fim", "Animal", "Setor", "Diagnóstico", "Status"]
        qs = Tratamento.objects.select_related("animal", "animal__setor", "diagnostico").order_by(
            "-data_inicio"
        )
        if data_inicio:
            qs = qs.filter(data_inicio__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data_inicio__lte=data_fim)
        if setor_id:
            qs = qs.filter(animal__setor_id=setor_id)

        linhas = []
        for t in qs:
            setor_str = t.animal.setor.nome if (t.animal and t.animal.setor) else "—"
            diag_str = t.diagnostico.nome if t.diagnostico else "—"
            linhas.append(
                [
                    formatar_data(t.data_inicio),
                    formatar_data(t.data_fim),
                    str(t.animal),
                    setor_str,
                    diag_str,
                    t.get_status_display() if hasattr(t, "get_status_display") else t.status,
                ]
            )

        kpis = [
            ("Total de tratamentos", len(linhas)),
            ("Em andamento", qs.filter(status="em_andamento").count()),
            ("Concluídos", qs.filter(status="concluido").count()),
        ]

    elif tipo == "vacinacoes":
        titulo = "Relatório de Vacinações e Vermifugações"
        colunas = ["Data", "Tipo", "Animal", "Setor", "Medicamento", "Próxima Aplicação"]
        qs_vac = Vacinacao.objects.select_related("animal", "animal__setor", "medicamento")
        qs_ver = Vermifugacao.objects.select_related("animal", "animal__setor", "medicamento")
        if data_inicio:
            qs_vac = qs_vac.filter(data__gte=data_inicio)
            qs_ver = qs_ver.filter(data__gte=data_inicio)
        if data_fim:
            qs_vac = qs_vac.filter(data__lte=data_fim)
            qs_ver = qs_ver.filter(data__lte=data_fim)
        if setor_id:
            qs_vac = qs_vac.filter(animal__setor_id=setor_id)
            qs_ver = qs_ver.filter(animal__setor_id=setor_id)

        linhas = []
        for v in qs_vac.order_by("-data"):
            setor_str = v.animal.setor.nome if (v.animal and v.animal.setor) else "—"
            med_str = v.medicamento.nome if v.medicamento else "—"
            linhas.append(
                [
                    formatar_data(v.data),
                    "Vacinação",
                    str(v.animal),
                    setor_str,
                    med_str,
                    formatar_data(v.proxima_dose),
                ]
            )

        for v in qs_ver.order_by("-data"):
            setor_str = v.animal.setor.nome if (v.animal and v.animal.setor) else "—"
            med_str = v.medicamento.nome if v.medicamento else "—"
            linhas.append(
                [
                    formatar_data(v.data),
                    "Vermifugação",
                    str(v.animal),
                    setor_str,
                    med_str,
                    formatar_data(v.proxima_aplicacao),
                ]
            )

        linhas.sort(key=lambda x: x[0], reverse=True)

        kpis = [
            ("Total de imunizações", len(linhas)),
            ("Vacinações", qs_vac.count()),
            ("Vermifugações", qs_ver.count()),
        ]

    elif tipo == "alimentacao":
        titulo = "Relatório de Consumo Alimentar por Setor"
        colunas = ["Data", "Setor", "Produto Alimentar", "Quantidade Consumida"]
        qs = ConsumoSetor.objects.select_related("setor", "produto").order_by("-data")
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        if setor_id:
            qs = qs.filter(setor_id=setor_id)

        linhas = []
        for c in qs:
            setor_str = c.setor.nome if c.setor else "—"
            prod_str = c.produto.nome if c.produto else "—"
            unidade = c.produto.unidade if c.produto and c.produto.unidade else "kg"
            linhas.append(
                [
                    formatar_data(c.data),
                    setor_str,
                    prod_str,
                    f"{c.quantidade} {unidade}",
                ]
            )

        kpis = [
            ("Registros de consumo", len(linhas)),
            ("Dietas ativas", Dieta.objects.filter(setor_id=setor_id).count() if setor_id else Dieta.objects.count()),
        ]

    else:
        titulo = "Relatório Geral Sanitário"
        colunas = ["Data", "Animal", "Setor", "Diagnóstico", "Sintomas"]
        linhas = []
        kpis = []

    return titulo, colunas, linhas, kpis


def gerar_pdf(titulo, colunas, dados, metadados):
    """Gera um PDF profissional com ReportLab no formato A4."""
    buffer = io.BytesIO()

    # Se houver mais de 5 colunas, usa landscape para não espremer o texto
    is_landscape = len(colunas) >= 5
    page_size = landscape(A4) if is_landscape else A4
    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )
    style_meta = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
    )
    style_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
    )
    style_header_cell = ParagraphStyle(
        "HeaderCell",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )

    story = []

    # Cabeçalho da Instituição
    instituicao_text = "<b>CAMPUS INTELIGENTE</b> · SISTEMA DE SANIDADE PECUÁRIA"
    story.append(
        Paragraph(
            instituicao_text,
            ParagraphStyle(
                "Sub",
                fontName="Helvetica-Bold",
                fontSize=9,
                textColor=colors.HexColor("#0f766e"),
                spaceAfter=2,
            ),
        )
    )
    story.append(Paragraph(titulo, style_title))

    # Linha de metadados (Setor, Período, Emissão, Usuário)
    meta_parts = []
    if metadados.get("setor"):
        meta_parts.append(f"<b>Setor:</b> {metadados['setor']}")
    if metadados.get("periodo"):
        meta_parts.append(f"<b>Período:</b> {metadados['periodo']}")
    meta_parts.append(f"<b>Emitido em:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    if metadados.get("usuario"):
        meta_parts.append(f"<b>Operador:</b> {metadados['usuario']}")

    story.append(Paragraph(" &nbsp;|&nbsp; ".join(meta_parts), style_meta))
    story.append(Spacer(1, 0.4 * cm))

    # Tabela de dados
    table_data = []
    # Header
    table_data.append([Paragraph(c, style_header_cell) for c in colunas])

    # Rows
    for row in dados:
        row_cells = []
        for cell in row:
            val_str = str(cell) if cell is not None else "—"
            row_cells.append(Paragraph(val_str, style_cell))
        table_data.append(row_cells)

    if not dados:
        vazio_cell = Paragraph(
            "<i>Nenhum registro encontrado para os filtros selecionados.</i>", style_cell
        )
        table_data.append([vazio_cell] + [""] * (len(colunas) - 1))

    # Larguras proporcionais
    page_usable_width = (page_size[0] - 3.0 * cm)
    col_width = page_usable_width / len(colunas)
    col_widths = [col_width] * len(colunas)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("LINEBELOW", (0, 0), (-1, 0), 1.2, colors.HexColor("#0d5e56")),
            ]
        )
    )
    story.append(t)

    # Resumo ao final
    story.append(Spacer(1, 0.4 * cm))
    total_text = f"<b>Total de registros listados:</b> {len(dados)}"
    story.append(Paragraph(total_text, style_meta))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()


def gerar_excel(titulo, colunas, dados, metadados):
    """Gera uma planilha XLSX nativa formatada com openpyxl."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório"

    # Cores
    header_fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
    header_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    meta_font = Font(name="Arial", size=9, bold=True, color="475569")
    title_font = Font(name="Arial", size=13, bold=True, color="0F172A")
    data_font = Font(name="Arial", size=9)

    border_thin = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )

    # Linhas de Cabeçalho / Metadados
    ws.append(["CAMPUS INTELIGENTE — SISTEMA DE SANIDADE PECUÁRIA"])
    ws.append([titulo])
    meta_info = f"Setor: {metadados.get('setor', 'Todos')} | Período: {metadados.get('periodo', 'Todos')} | Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    ws.append([meta_info])
    ws.append([])  # Linha em branco

    # Formatação do bloco de título
    ws.cell(row=1, column=1).font = Font(name="Arial", size=9, bold=True, color="0F766E")
    ws.cell(row=2, column=1).font = title_font
    ws.cell(row=3, column=1).font = meta_font

    # Cabeçalho da tabela (linha 5)
    header_row_idx = 5
    ws.append(colunas)
    for col_idx in range(1, len(colunas) + 1):
        cell = ws.cell(row=header_row_idx, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border_thin

    # Linhas de Dados
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    current_row = header_row_idx + 1
    for row in dados:
        ws.append(row)
        for col_idx in range(1, len(colunas) + 1):
            cell = ws.cell(row=current_row, column=col_idx)
            cell.font = data_font
            cell.border = border_thin
            cell.alignment = Alignment(vertical="center")
            if (current_row % 2) == 0:
                cell.fill = zebra_fill
        current_row += 1

    if not dados:
        ws.append(["Nenhum registro encontrado para os filtros selecionados."])
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(colunas))
        cell = ws.cell(row=current_row, column=1)
        cell.font = Font(name="Arial", size=9, italic=True, color="94A3B8")
        current_row += 1

    # Linha final de Total
    current_row += 1
    ws.cell(row=current_row, column=1, value=f"Total de registros: {len(dados)}").font = Font(
        name="Arial", size=9, bold=True, color="0F172A"
    )

    # Ajuste automático de largura de colunas
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            # Ignora as 4 primeiras linhas de título no cálculo de largura
            if cell.row < header_row_idx:
                continue
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


@login_required
def central_relatorios(request):
    """View principal da Central de Relatórios: visualização interativa e exportação (PDF/Excel)."""
    # Se o usuário possui setor fixo no cadastro (ex: Caprinocultura), força o setor dele
    user_setor_fixo = hasattr(request.user, "perfil") and request.user.perfil.setor
    setor_atual = None

    if user_setor_fixo:
        setor_id = str(request.user.perfil.setor.pk)
        setor_atual = request.user.perfil.setor
    else:
        setor_id = request.GET.get("setor_id", "").strip() or request.session.get("setor_id", "")
        if setor_id:
            setor_atual = Setor.objects.filter(pk=setor_id).first()

    tipo = request.GET.get("tipo", "ocorrencias").strip()

    # Período padrão: últimos 30 dias até hoje
    hoje = date.today()
    data_inicio_str = request.GET.get("data_inicio", "")
    data_fim_str = request.GET.get("data_fim", "")

    if data_inicio_str:
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
        except ValueError:
            data_inicio = hoje - timedelta(days=30)
    else:
        data_inicio = hoje - timedelta(days=30)
        data_inicio_str = data_inicio.strftime("%Y-%m-%d")

    if data_fim_str:
        try:
            data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d").date()
        except ValueError:
            data_fim = hoje
    else:
        data_fim = hoje
        data_fim_str = data_fim.strftime("%Y-%m-%d")

    formato = request.GET.get("formato", "").lower().strip()

    titulo, colunas, dados, kpis = coletar_dados_relatorio(tipo, data_inicio, data_fim, setor_id)

    metadados = {
        "setor": setor_atual.nome if setor_atual else "Todos os setores",
        "periodo": f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
        "usuario": request.user.get_full_name() or request.user.username,
    }

    # Exportação em PDF
    if formato == "pdf":
        pdf_bytes = gerar_pdf(titulo, colunas, dados, metadados)
        RelatorioSanitario.objects.create(
            tipo=f"{titulo} (PDF)",
            periodo_inicio=data_inicio,
            periodo_fim=data_fim,
            usuario=request.user,
        )
        LogAuditoria.objects.create(
            usuario=request.user,
            acao="Exportação de Relatório (PDF)",
            descricao=f"Relatório {titulo} exportado em PDF para {metadados['setor']}.",
        )
        filename = f"relatorio_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    # Exportação em Planilha (Excel)
    if formato in ("excel", "xlsx", "planilha"):
        excel_bytes = gerar_excel(titulo, colunas, dados, metadados)
        RelatorioSanitario.objects.create(
            tipo=f"{titulo} (Excel)",
            periodo_inicio=data_inicio,
            periodo_fim=data_fim,
            usuario=request.user,
        )
        LogAuditoria.objects.create(
            usuario=request.user,
            acao="Exportação de Relatório (Excel)",
            descricao=f"Relatório {titulo} exportado em XLSX para {metadados['setor']}.",
        )
        filename = f"relatorio_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        response = HttpResponse(
            excel_bytes,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    context = {
        "active": "relatorio",
        "tipo_selecionado": tipo,
        "data_inicio": data_inicio_str,
        "data_fim": data_fim_str,
        "setor_id_selecionado": setor_id,
        "setor_atual": setor_atual,
        "setor_fixo": bool(user_setor_fixo),
        "setores": Setor.objects.all().order_by("nome"),
        "titulo_relatorio": titulo,
        "colunas": colunas,
        "dados": dados,
        "total_registros": len(dados),
        "kpis": kpis,
        "historico_recente": RelatorioSanitario.objects.select_related("usuario").order_by("-data_geracao")[:5],
    }
    return render(request, "sanitario/relatorios_central.html", context)
