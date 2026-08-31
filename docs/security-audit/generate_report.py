#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Relatório de Auditoria de Segurança — Maquiadora Sue
Gera PDF A4 com capa, resumo executivo (gráficos), pontos fortes/fracos, achados e issues.
Paleta: crítica #B91C1C, alta #EA580C, média #D97706, baixa #2563EB, ponto forte #059669
"""
import os
import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT_DIR = Path(__file__).parent
OUT_PDF = OUT_DIR / "relatorio-auditoria-seguranca.pdf"
IMG_DONUT = OUT_DIR / "_donut.png"
IMG_BARS = OUT_DIR / "_bars.png"

# Palette
C_CRITICA = HexColor("#B91C1C")
C_ALTA = HexColor("#EA580C")
C_MEDIA = HexColor("#D97706")
C_BAIXA = HexColor("#2563EB")
C_FORTE = HexColor("#059669")
C_GOLD = HexColor("#C5A059")
C_DARK = HexColor("#1C1C1C")
C_MUTED = HexColor("#555555")
C_BG = HexColor("#FDFBF9")
C_BORDER = HexColor("#EFEBE4")

PROJECT_NAME = "Maquiadora Sue Website"
DATA_AUDITORIA = "30 de agosto de 2026"
ESCOPO = "site_maquiadora_sue.html, site_maquiadora_sue_en.html, biosite.html, shared.css, site.css, biosite.css, fontawesome.css, record_site.js, configs e histórico git"
AUDITOR = "Muse Spark — Auditoria automatizada + revisão manual"

# --- Achados sumarizados ---
# severity counts
severity_counts = {
    "Crítica": 0,
    "Alta": 1,
    "Média": 2,
    "Baixa": 2,
    "Informativa": 1,
}
# maps for chart
sev_labels = ["Alta", "Média", "Baixa", "Informativa"]
sev_values = [1, 2, 2, 1]
sev_colors = ["#EA580C", "#D97706", "#2563EB", "#6B7280"]

cat_labels = ["Banco\nsem tranca", "Chaves\nexpostas", "Inputs\n(XSS/CSP)", "Headers/\nClickjacking", "PII/\nInfo leak"]
cat_values = [1, 1, 1, 2, 1]
cat_colors = ["#EA580C", "#D97706", "#2563EB", "#92400E", "#059669"]

# --- Helpers para gráficos ---
def gen_donut():
    fig, ax = plt.subplots(figsize=(3.2, 3.2), dpi=180)
    fig.patch.set_facecolor('white')
    # donut
    wedges, texts, autotexts = ax.pie(
        sev_values,
        labels=None,
        autopct=lambda p: f'{p:.0f}%' if p>0 else '',
        startangle=90,
        colors=sev_colors,
        wedgeprops=dict(width=0.48, edgecolor='white', linewidth=2),
        pctdistance=0.82,
        textprops=dict(fontsize=9, color='#1C1C1C', weight='bold')
    )
    centre = plt.Circle((0,0), 0.52, fc='white')
    ax.add_artist(centre)
    total = sum(sev_values)
    ax.text(0, 0.06, str(total), ha='center', va='center', fontsize=22, weight='bold', color='#1C1C1C')
    ax.text(0, -0.14, 'achados', ha='center', va='center', fontsize=9, color='#6B7280')
    # legend outside
    leg_labels = [f"{l} ({v})" for l,v in zip(sev_labels, sev_values)]
    ax.legend(wedges, leg_labels, loc='center', bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False, fontsize=8)
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig(IMG_DONUT, bbox_inches='tight', facecolor='white')
    plt.close()

def gen_bars():
    fig, ax = plt.subplots(figsize=(5.2, 2.8), dpi=180)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    bars = ax.bar(cat_labels, cat_values, color=cat_colors, edgecolor='white', linewidth=1.2, width=0.62)
    for bar, v in zip(bars, cat_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.06, str(v), ha='center', va='bottom', fontsize=9, weight='bold', color='#1C1C1C')
    ax.set_ylim(0, max(cat_values)+1.0)
    ax.set_ylabel('Qtd. achados', fontsize=8, color='#555555')
    ax.tick_params(axis='x', labelsize=7, colors='#1C1C1C')
    ax.tick_params(axis='y', labelsize=7, colors='#6B7280')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E7EB')
    ax.spines['bottom'].set_color('#E5E7EB')
    ax.yaxis.grid(True, color='#F3F4F6', linewidth=0.8)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(IMG_BARS, bbox_inches='tight', facecolor='white')
    plt.close()

gen_donut()
gen_bars()

# --- PDF styles ---
styles = getSampleStyleSheet()
sTitle = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=22, leading=26, textColor=C_DARK, alignment=TA_CENTER, fontName='Helvetica-Bold')
sSubtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, leading=14, textColor=C_MUTED, alignment=TA_CENTER, fontName='Helvetica')
sH1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, leading=17, textColor=C_DARK, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=8, keepWithNext=True, borderPadding=(0,0,6,0))
sH2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=C_DARK, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6)
sH3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=10, leading=13, textColor=C_DARK, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)
sBody = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8.5, leading=12.5, textColor=HexColor("#222222"), alignment=TA_JUSTIFY, fontName='Helvetica', spaceAfter=4)
sBodySmall = ParagraphStyle('BodySmall', parent=sBody, fontSize=7.5, leading=10.5)
sBullet = ParagraphStyle('Bullet', parent=sBody, leftIndent=14, bulletIndent=6, spaceAfter=2)
sCell = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=7, leading=9, textColor=HexColor("#1F2937"), fontName='Helvetica', alignment=TA_LEFT)
sCellSmall = ParagraphStyle('CellSmall', parent=sCell, fontSize=6.2, leading=8)
sHeaderCell = ParagraphStyle('HeaderCell', parent=sCell, textColor=colors.white, fontName='Helvetica-Bold', alignment=TA_CENTER, fontSize=7)
sFooter = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=6.5, leading=8, textColor=HexColor("#6B7280"), alignment=TA_CENTER, fontName='Helvetica')
sCaption = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=6.5, leading=8, textColor=HexColor("#6B7280"), alignment=TA_CENTER, fontName='Helvetica-Oblique')
sChip = ParagraphStyle('Chip', parent=styles['Normal'], fontSize=6.5, leading=7, textColor=colors.white, alignment=TA_CENTER, fontName='Helvetica-Bold')
sMono = ParagraphStyle('Mono', parent=styles['Normal'], fontSize=6.5, leading=8.5, textColor=HexColor("#1F2937"), fontName='Courier', backColor=HexColor("#F9FAFB"), borderPadding=(3,3,3))

def chip(text, bg):
    # returns a Paragraph that looks like a chip via table with background
    inner = Paragraph(f'<font color="white"><b>{text}</b></font>', sChip)
    t = Table([[inner]], colWidths=[38])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('ROUNDEDCORNERS', [4,4,4,4]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    return t

def severity_chip_table(sev):
    m = {"Alta": C_ALTA, "Média": C_MEDIA, "Baixa": C_BAIXA, "Informativa": HexColor("#6B7280"), "Crítica": C_CRITICA}
    bg = m.get(sev, C_BAIXA)
    return chip(sev.upper(), bg)

# Header/footer
def header_footer(canvas, doc):
    canvas.saveState()
    # header line
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(20*mm, 282*mm, 190*mm, 282*mm)
    canvas.setFont('Helvetica', 6)
    canvas.setFillColor(HexColor("#6B7280"))
    canvas.drawString(20*mm, 286*mm, "Relatório de Auditoria de Segurança — Maquiadora Sue Website")
    canvas.drawRightString(190*mm, 286*mm, DATA_AUDITORIA)
    # footer line
    canvas.line(20*mm, 14*mm, 190*mm, 14*mm)
    canvas.setFont('Helvetica', 6)
    canvas.drawCentredString(105*mm, 10*mm, f"Página {doc.page}")
    canvas.setFont('Helvetica-Oblique', 5.5)
    canvas.drawRightString(190*mm, 10*mm, "Confidencial — uso interno")
    canvas.restoreState()

def cover_footer(canvas, doc):
    # only footer for cover
    canvas.saveState()
    canvas.setFont('Helvetica', 6)
    canvas.setFillColor(HexColor("#6B7280"))
    canvas.drawCentredString(105*mm, 10*mm, "Documento gerado automaticamente — validar achados antes de publicar issues")
    canvas.restoreState()

# Build story
story = []

# CAPA
story.append(Spacer(1, 22*mm))
# Logo-like badge
badge_data = [[Paragraph('<font color="#C5A059"><b>◆</b></font>  MAQUIADORA SUE', ParagraphStyle('badge', parent=styles['Normal'], fontSize=7, leading=9, textColor=C_MUTED, alignment=TA_CENTER, fontName='Helvetica'))]]
badge_tbl = Table(badge_data, colWidths=[70*mm])
badge_tbl.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.6, C_BORDER),
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
# center badge
wrapper = Table([[badge_tbl]], colWidths=[170*mm])
wrapper.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
story.append(wrapper)
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Relatório de Auditoria<br/>de Segurança", ParagraphStyle('coverTitle', parent=sTitle, fontSize=26, leading=30, alignment=TA_CENTER, textColor=C_DARK)))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Maquiadora Sue Website", ParagraphStyle('coverSub', parent=styles['Normal'], fontSize=11, leading=14, textColor=C_GOLD, alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width=22*mm, thickness=1.2, lineCap='round', color=C_GOLD, spaceAfter=6, spaceBefore=6, hAlign='CENTER', vAlign='BOTTOM', dash=None))
story.append(Paragraph(f"{DATA_AUDITORIA}  •  v1.0  •  Escopo estático (sem backend)", sSubtitle))
story.append(Spacer(1, 12*mm))
# Info box
info_style = ParagraphStyle('infoBox', parent=sBodySmall, fontSize=7.5, leading=11, textColor=HexColor("#1F2937"), alignment=TA_LEFT)
info_rows = [
    [Paragraph("<b>Escopo auditado</b>", sCellSmall), Paragraph(ESCOPO, sCellSmall)],
    [Paragraph("<b>Metodologia</b>", sCellSmall), Paragraph("Auditoria manual linha-a-linha + grep automatizado (5 categorias OWASP-adaptadas). Cada categoria mapeada para a stack real (site estático HTML/CSS/JS). Sem especulação: todo achado traz arquivo:linha e trecho.", sCellSmall)],
    [Paragraph("<b>Stack detectada</b>", sCellSmall), Paragraph("<b>Frontend:</b> HTML5 + CSS3 + Vanilla JS (IIFE, sem framework/build). <b>Backend/Banco/Auth:</b> inexistentes (site 100% estático). <b>Deploy:</b> sem Dockerfile/CI/Helm/Terraform/.env. <b>CDN:</b> FontAwesome 6.4.0 (com SRI) + Google Fonts. <b>Hospedagem presumida:</b> static hosting (ex: GitHub Pages).", sCellSmall)],
    [Paragraph("<b>Auditor</b>", sCellSmall), Paragraph(AUDITOR, sCellSmall)],
]
info_tbl = Table(info_rows, colWidths=[32*mm, 118*mm])
info_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), HexColor("#FDFBF9")),
    ('BACKGROUND', (1,0), (1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 0.6, C_BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.4, C_BORDER),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, HexColor("#FFFBF5")]),
]))
story.append(info_tbl)
story.append(Spacer(1, 8*mm))
# Nota metodológica
story.append(Paragraph(
    "<b>Nota metodológica — mapeamento das 5 categorias para esta stack:</b><br/>"
    "<b>1) Banco sem tranca</b> → isolamento de arquivos estáticos sensíveis (sem RLS/tenant; verifica exposição de PDFs/imagens privadas no document root). &nbsp;"
    "<b>2) Permissão no navegador</b> → gates de papel (isAdmin/canEdit) sem validação servidor — <i>não aplicável (sem backend)</i>. &nbsp;"
    "<b>3) IDOR</b> → acesso direto a objetos por nome/ID previsível — <i>não aplicável no sentido API, adaptado para enumeration de arquivos</i>. &nbsp;"
    "<b>4) Chaves expostas</b> → varredura de secrets em código, configs, git e bundle. &nbsp;"
    "<b>5) Inputs sem tratamento (XSS)</b> → innerHTML/eval/v-html/URLs javascript: e sanitização no frontend/backend.",
    ParagraphStyle('nota', parent=sBodySmall, fontSize=6.8, leading=10, textColor=HexColor("#4B5563"), alignment=TA_JUSTIFY, borderPadding=(6,6,6), backColor=HexColor("#FFFBF5"))
))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("Classificação: <font color=\"#059669\"><b>CONFIDENCIAL</b></font> — compartilhar apenas com responsáveis técnicos e de negócio.", ParagraphStyle('classif', parent=sBodySmall, fontSize=7, leading=10, textColor=C_MUTED, alignment=TA_CENTER)))
# next page with header/footer
story.append(PageBreak())

# SUMÁRIO EXECUTIVO
story.append(Paragraph("Resumo executivo", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=4, spaceBefore=0))
story.append(Paragraph(
    "Site 100% estático, sem backend, banco ou autenticação. Das 5 categorias, <b>2 não se aplicam</b> (não há superfície de ataque para RLS/tenant, RBAC servidor ou IDOR de API) — prova de cobertura, não omissão. "
    "Foram confirmados <b>6 achados</b> (0 críticos): 1 alta, 2 média, 2 baixa, 1 informativa. O risco central é <b>exposição de documentos de negócio</b> (orçamentos em PDF versionados e servidos no web root) "
    "combinada com <b>headers de segurança incompletos</b> (CSP com <i>unsafe-inline</i> e sem <i>frame-ancestors/object-src/base-uri</i>, ausência de HSTS/X-Frame-Options via HTTP). "
    "Não há XSS via innerHTML/eval nem segredos hardcoded; todos os <i>target=_blank</i> usam <i>rel=noopener</i>. Correção priorizada: remover PDFs do deploy e endurecer headers/CSP.",
    sBody
))
story.append(Spacer(1, 3*mm))
# KPI cards
kpi_data = [
    [Paragraph("<b><font color=\"#B91C1C\" size=14>0</font></b><br/><font color=\"#6B7280\" size=7>CRÍTICA</font>", ParagraphStyle('kpi', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, leading=10, fontName='Helvetica')),
     Paragraph("<b><font color=\"#EA580C\" size=14>1</font></b><br/><font color=\"#6B7280\" size=7>ALTA</font>", ParagraphStyle('kpi2', parent=styles['Normal'], alignment=TA_CENTER)),
     Paragraph("<b><font color=\"#D97706\" size=14>2</font></b><br/><font color=\"#6B7280\" size=7>MÉDIA</font>", ParagraphStyle('kpi3', parent=styles['Normal'], alignment=TA_CENTER)),
     Paragraph("<b><font color=\"#2563EB\" size=14>2</font></b><br/><font color=\"#6B7280\" size=7>BAIXA</font>", ParagraphStyle('kpi4', parent=styles['Normal'], alignment=TA_CENTER)),
     Paragraph("<b><font color=\"#6B7280\" size=14>1</font></b><br/><font color=\"#6B7280\" size=7>INFORMATIVA</font>", ParagraphStyle('kpi5', parent=styles['Normal'], alignment=TA_CENTER)),
     Paragraph("<b><font color=\"#059669\" size=14>7</font></b><br/><font color=\"#6B7280\" size=7>PONTOS FORTES</font>", ParagraphStyle('kpi6', parent=styles['Normal'], alignment=TA_CENTER))],
]
kpi_tbl = Table(kpi_data, colWidths=[26*mm, 26*mm, 26*mm, 26*mm, 26*mm, 26*mm])
kpi_tbl.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.6, C_BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.4, C_BORDER),
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(kpi_tbl)
story.append(Spacer(1, 4*mm))
# Gráficos
story.append(Paragraph("Distribuição por severidade e por categoria", sH2))
# place images side by side
img_tbl = Table([
    [Image(str(IMG_DONUT), width=62*mm, height=62*mm), Image(str(IMG_BARS), width=84*mm, height=46*mm)]
], colWidths=[72*mm, 88*mm])
img_tbl.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(img_tbl)
story.append(Paragraph("Figura 1 — Rosca por severidade (esq.) e barras por categoria mapeada (dir.). Paleta: crítica #B91C1C, alta #EA580C, média #D97706, baixa #2563EB, ponto forte #059669.", sCaption))
story.append(Spacer(1, 3*mm))
# Mini resumo textual
story.append(Paragraph(
    "<b>Leitura rápida:</b> 83% dos achados são de endurecimento (headers/CSP/PII) — baixo custo de correção e alto ganho. "
    "O único achado de severidade <b>Alta</b> é processual (higiene de repositório/deploy), não falha de código XSS/IDOR.",
    ParagraphStyle('leitura', parent=sBodySmall, backColor=HexColor("#F0FDF4"), borderPadding=(5,5,5), textColor=HexColor("#065F46"))
))

# PONTOS FORTES E PONTOS FRACOS
story.append(Paragraph("Pontos fortes (o que está protegido)", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=3, spaceBefore=0))
fortes = [
    ("<b>PF-01 — Sem superfície de IDOR/Banco/RBAC:</b> projeto sem backend, sem ORM/query builder, sem autenticação e sem rotas com ID — categorias 1, 2 e 3 verificadas arquivo-a-arquivo e confirmadas como <i>não aplicáveis</i> (prova de cobertura).", "Verificado em: site_maquiadora_sue.html, biosite.html, record_site.js, ausência total de fetch/XHR/API em todo o código."),
    ("<b>PF-02 — target=_blank sempre com rel=noopener noreferrer:</b> 21/21 links externos (7 por página × 3 páginas) blindados contra tabnabbing.", "biosite.html:72,78,84,90,100,101,102; site_maquiadora_sue.html:136,151,444,460,468,469,487 (todos com <i>rel=\"noopener noreferrer\"</i>)."),
    ("<b>PF-03 — Zero innerHTML/eval/v-html/javascript::</b> grep em todo o repo retornou 0 ocorrências; lightbox manipula DOM apenas via <i>.src/.alt/.classList</i>, nunca via HTML.", "site_maquiadora_sue.html:527-528 <i>lbImg.src = img.src; lbImg.alt = img.alt;</i>; grep <i>innerHTML|eval(|new Function|javascript:</i> = 0 hits."),
    ("<b>PF-04 — SRI + crossorigin no CDN:</b> FontAwesome 6.4.0 pinado com integridade, mitigando supply-chain.", "site_maquiadora_sue.html:102-103 <i>integrity=\"sha512-iecdLmaskl7CVk...\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"</i> (idem EN:102-103)."),
    ("<b>PF-05 — Headers meta presentes:</b> CSP + X-Content-Type-Options + Referrer-Policy em todas as páginas.", "site_maquiadora_sue.html:12-14, biosite.html:10-12, EN:12-14."),
    ("<b>PF-06 — Sem segredos hardcoded:</b> varredura de <i>api_key/secret/password/token/AKIA/ghp_/sk-/BEGIN PRIVATE</i> = 0 hits no código e no histórico git (5 commits inspecionados).", "Grep global 0 hits; <i>git log --patch</i> sem credenciais; GA4 placeholder permanece comentado (<i>G-XXXXXXXXXX</i>)."),
    ("<b>PF-07 — WhatsApp CTAs com texto estático:</b> parâmetros <i>text=</i> não refletem input do usuário, sem reflexão.", "site_maquiadora_sue.html:136,151,444,487 etc. — strings literais, sem concatenação de query string do usuário."),
]
for txt, ev in fortes:
    story.append(Paragraph(f"<font color=\"#059669\">✔</font> {txt}", sBodySmall))
    story.append(Paragraph(f"<font color=\"#6B7280\"><i>Evidência: {ev}</i></font>", ParagraphStyle('ev', parent=sBodySmall, fontSize=6.5, leading=8, textColor=HexColor("#6B7280"), leftIndent=10)))
    story.append(Spacer(1,1*mm))

story.append(Paragraph("Pontos fracos (riscos centrais)", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=3, spaceBefore=0))
fracos = [
    ("<b>Exposição de documentos de negócio:</b> PDFs de orçamento (inclui caso nominal “Helena 2026”) versionados com <i>git</i> e presentes no document root — qualquer deploy estático os serve publicamente, vazando pricing e dado pessoal.", "ALTA"),
    ("<b>CSP com unsafe-inline e sem diretivas críticas:</b> <i>script-src 'unsafe-inline'</i> anula boa parte do ganho anti-XSS; faltam <i>object-src 'none'</i>, <i>base-uri 'self'</i>, <i>frame-ancestors 'self'</i>.", "MÉDIA"),
    ("<b>Headers só via &lt;meta&gt;:</b> sem HSTS, X-Frame-Options/frame-ancestors via HTTP e Permissions-Policy — clickjacking e downgrade permanecem possíveis conforme servidor.", "MÉDIA"),
    ("<b>PII em plain text + JSON-LD:</b> e-mail e telefone em HTML favorecem scraping/spam; sem ofuscação.", "BAIXA"),
    ("<b>Higiene de deploy:</b> <i>getImages</i> e <i>Shooting (n).jpeg</i> brutos + backups <i>*.bak</i> (gitignore cobre mas histórico permanece) aumentam superfície e custo de crawl.", "BAIXA"),
]
for txt, sev in fracos:
    chip_tbl = severity_chip_table(sev)
    row = Table([[Paragraph(txt, sBodySmall), chip_tbl]], colWidths=[132*mm, 22*mm])
    row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('LEFTPADDING', (1,0), (1,0), 2),
    ]))
    story.append(row)
    story.append(Spacer(1,1.5*mm))

# TABELA DE ACHADOS DETALHADOS
story.append(Paragraph("Achados detalhados por categoria", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=2, spaceBefore=0))
story.append(Paragraph(
    "Cada linha traz <b>Severidade | Arquivo:linha | Descrição + trecho + por que é explorável</b>. "
    "Condição de explorabilidade indicada quando depende de config de deploy.",
    sBodySmall
))
# header
header = [
    Paragraph("<b>SEV.</b>", sHeaderCell),
    Paragraph("<b>ARQUIVO:LINHA</b>", sHeaderCell),
    Paragraph("<b>CATEGORIA — DESCRIÇÃO, TRECHO E EXPLORABILIDADE</b>", sHeaderCell),
]
rows = [header]

# helper to add row
def sev_chip_cell(s): 
    return severity_chip_table(s)

# A-01
rows.append([
    sev_chip_cell("Alta"),
    Paragraph("ORÇAMENTO 2026 -<br/>DEBUTANTE.pdf.pdf<br/>(git ls-files)<br/>Orçamento Noiva<br/>Helena 2026..pdf", sCellSmall),
    Paragraph(
        "<b>[Cat. 1 — Banco sem tranca / Cat. 4 — Chaves/PII] Documentos sensíveis no web root e no git</b><br/>"
        "<b>Trecho/estado:</b> <font face=\"Courier\" size=6>git ls-files | grep pdf → \"ORÇAMENTO…pdf\" (4,4 MB) + \"Orçamento Noiva Helena 2026..pdf\" (12,8 MB) — ambos <i>tracked</i></font><br/>"
        "<b>Por que é explorável:</b> hosting estático serve tudo no diretório; /ORÇAMENTO…pdf é baixável por qualquer visitante/crawler. Vaza tabela de preços 2026 e dado pessoal de cliente (Helena). Histórico git preserva mesmo após remoção do deploy.<br/>"
        "<b>Condição:</b> explorável se repositório for publicado ou pasta for deployada (GitHub Pages/Netlify/Vercel com root = repo).",
        sCellSmall),
])
# A-02
rows.append([
    sev_chip_cell("Média"),
    Paragraph("site_maquiadora_sue.html:12<br/>site_maquiadora_sue_en.html:12<br/>biosite.html:10", sCellSmall),
    Paragraph(
        "<b>[Cat. 5 — Inputs/CSP] CSP com 'unsafe-inline' e sem object-src/base-uri/frame-ancestors</b><br/>"
        "<b>Trecho:</b> <font face=\"Courier\" size=6>content=\"default-src 'self'; … script-src 'self' 'unsafe-inline' https://www.googletagmanager.com …\"</font><br/>"
        "<b>Por que é explorável:</b> <i>unsafe-inline</i> permite execução de qualquer script inline injetado (se um dia houver user-content ou CMS). Falta <i>object-src 'none'</i> (permite &lt;object&gt;/Flash), <i>base-uri 'self'</i> (permite injeção de &lt;base&gt;) e <i>frame-ancestors</i> (clickjacking). Severidade média pois hoje não há vetor de injeção (PF-03), mas endurecimento é preventivo de alto ROI.<br/>"
        "<b>Condição:</b> vira alta se o site passar a renderizar conteúdo dinâmico (CMS, query-reflection, comentários).",
        sCellSmall),
])
# A-03
rows.append([
    sev_chip_cell("Média"),
    Paragraph("site_maquiadora_sue.html:13-14<br/>biosite.html:11-12<br/>(ausência via HTTP)", sCellSmall),
    Paragraph(
        "<b>[Cat. 5 — Headers] Segurança dependente só de &lt;meta&gt; — sem HSTS/X-Frame-Options via header HTTP</b><br/>"
        "<b>Trecho:</b> <font face=\"Courier\" size=6>&lt;meta http-equiv=\"X-Content-Type-Options\" content=\"nosniff\"&gt; + CSP via meta</font> — sem <i>Strict-Transport-Security</i>, <i>X-Frame-Options</i> ou <i>Permissions-Policy</i>.<br/>"
        "<b>Por que é explorável:</b> &lt;meta&gt; não é respeitado para HSTS e tem precedência menor que header HTTP; site pode ser iframado para clickjacking (ex: CTA WhatsApp sobreposto) e não força HTTPS em subrequests. Exploração requer que o servidor estático não injete headers (comum em Pages sem _headers).<br/>"
        "<b>Condição:</b> depende do host — mitigável com <i>_headers</i> (Netlify) / <i>vercel.json</i> / config S3/CloudFront.",
        sCellSmall),
])
# A-04
rows.append([
    sev_chip_cell("Baixa"),
    Paragraph("site_maquiadora_sue.html:49,461<br/>biosite.html:—<br/>JSON-LD 48-49", sCellSmall),
    Paragraph(
        "<b>[Cat. 4 — Chaves/PII] E-mail e telefone em plain text no HTML e JSON-LD</b><br/>"
        "<b>Trecho:</b> <font face=\"Courier\" size=6>\"email\": \"suelimamakeup@gmail.com\" / &lt;a href=\"mailto:suelimamakeup@gmail.com\"&gt; / +55-21-99542-1808</font> (8 ocorrências de wa.me/5521995421808)<br/>"
        "<b>Por que é explorável:</b> não é vazamento de segredo, mas PII de negócio exposto a scrapers/spam/phishing de marca (BEC). JSON-LD facilita extração automatizada. Risco baixo e intencional (contato comercial), mas documentado para decisão consciente. Mitigação opcional: ofuscação JS ou form com backend.",
        sCellSmall),
])
# A-05
rows.append([
    sev_chip_cell("Baixa"),
    Paragraph("site_maquiadora_sue.html:98-99<br/>biosite.html:33-34", sCellSmall),
    Paragraph(
        "<b>[Cat. 4/5 — Supply-chain / Referrer] Google Fonts sem SRI + Referrer-Policy permissiva + onload trick</b><br/>"
        "<b>Trecho:</b> <font face=\"Courier\" size=6>&lt;link href=\"https://fonts.googleapis.com/css2?...\" media=\"print\" onload=\"this.media='all'\"&gt;</font> sem <i>integrity</i>; <font face=\"Courier\" size=6>Referrer-Policy: origin-when-cross-origin</font><br/>"
        "<b>Por que é explorável:</b> Google Fonts não oferece hash estável (SRI impraticável) — risco de supply-chain se CDN for comprometida; <i>origin-when-cross-origin</i> vaza <i>path/query</i> para Google/CDN/tiktok/instagram ao clicar. Baixa severidade; mitigação é self-host de fonts (já feito no biosite) e <i>strict-origin-when-cross-origin</i> ou <i>strict-origin</i>.",
        sCellSmall),
])
# A-06
rows.append([
    Paragraph("<b><font color=\"#6B7280\">INFO</font></b>", ParagraphStyle('infoChip', parent=sHeaderCell, textColor=HexColor("#6B7280"))),
    Paragraph("site_maquiadora_sue.html:17-18,84-93<br/>git history", sCellSmall),
    Paragraph(
        "<b>[Cat. 4 — Higiene] Placeholders comentados (G-XXXXXXXXXX / CÓDIGO_AQUI) + arquivos de mídia brutos no repo</b><br/>"
        "<b>Trecho:</b> <font face=\"Courier\" size=6>&lt;!-- &lt;script gtag/js?id=G-XXXXXXXXXX&gt; --&gt;</font> e <font face=\"Courier\" size=6>gemini-code-1783942303074.html (0 bytes)</font> + 22× <i>Shooting (n).jpeg</i> (2-4 MB cada).<br/>"
        "<b>Por que é relevante:</b> placeholder inofensivo hoje, mas se ativado com ID real sem remover comentário de GSC, facilita hijack de Analytics/Search Console. Arquivos pesados aumentam tempo/build e podem ser enumerados. Informativo — agrupado para não gerar spam de issues.",
        sCellSmall),
])

# build table with styles
col_ws = [18*mm, 32*mm, 110*mm]
t = Table(rows, colWidths=col_ws, repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), C_DARK),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor("#F9FAFB")]),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "<i>Categorias 2 (Permissão no navegador) e 3 (IDOR) — não aplicáveis:</i> varredura completa de handlers (0 rotas backend) confirma ausência de superfície. Registrado como <b>pontos fortes PF-01/PF-03</b>, não omissão.",
    ParagraphStyle('na', parent=sBodySmall, fontSize=6.5, leading=8, textColor=HexColor("#065F46"), backColor=HexColor("#ECFDF5"), borderPadding=(4,4,4))
))

# RECOMENDAÇÕES PRIORIZADAS
story.append(Paragraph("Recomendações priorizadas", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=2, spaceBefore=0))
recs = [
    ("P1 — Remover PDFs sensíveis do web root e do git", "ALTA", "Mover <i>ORÇAMENTO…pdf</i> e <i>Orçamento Helena</i> para storage privado (Drive com link restrito) ou pasta fora do deploy; fazer <i>git rm --cached</i> + <i>git filter-repo</i>/BFG para limpar histórico; adicionar <i>*.pdf</i> ao .gitignore (ou allowlist só para PDFs públicos); configurar deploy para ignorar /docs internos. Se precisar expor, servir via endpoint com auth ou link temporário."),
    ("P2 — Endurecer CSP (eliminar unsafe-inline)", "MÉDIA", "Extrair JS inline (linhas 491-656) para <i>site.js</i> externo; gerar hash/nonce e trocar <i>script-src 'self' 'unsafe-inline'</i> por <i>script-src 'self' 'sha256-…'</i>; adicionar <i>object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self' https://wa.me https://api.whatsapp.com; upgrade-insecure-requests</i>. Testar com <i>Content-Security-Policy-Report-Only</i> antes."),
    ("P3 — Headers via HTTP (não só meta)", "MÉDIA", "No host estático, criar <i>_headers</i> (Netlify) / <i>vercel.json</i> / <i>.htaccess</i> com: <i>Strict-Transport-Security: max-age=31536000; includeSubDomains; preload</i>, <i>X-Frame-Options: SAMEORIGIN</i> (ou <i>frame-ancestors</i> na CSP), <i>Permissions-Policy: camera=(), microphone=(), geolocation=()</i>, <i>Referrer-Policy: strict-origin-when-cross-origin</i>. Remover CSP de &lt;meta&gt; após migrar para header."),
    ("P4 — Self-host Google Fonts (opcional)", "BAIXA", "Já feito no biosite (fontawesome.css self-hosted). Aplicar ao Lato/Playfair: baixar woff2, servir de <i>/fonts</i> com <i>font-display: swap</i>. Elimina dependência de CDN, permite SRI/cache e reduz vazamento de referrer. Se manter CDN, trocar Referrer-Policy para <i>strict-origin-when-cross-origin</i>."),
    ("P5 — Higiene de repositório e .gitignore", "BAIXA", "Adicionar <i>*.pdf</i>, <i>Shooting*.jpeg</i> brutos e <i>gemini-*.html</i> ao .gitignore; manter apenas <i>*.webp</i> otimizados no deploy; mover roteiros (.md) para <i>/docs</i> com deploy ignorando a pasta; habilitar <i>secret scanning</i> (GitHub push protection)."),
    ("P6 — Ofuscação leve de PII (se desejado)", "INFORMATIVA", "Se spam aumentar, trocar <i>mailto:</i> por formulário (Formspree/Netlify Forms) ou ofuscar e-mail via JS (ex: <i>data-email</i> + decode). Avaliar trade-off SEO (JSON-LD precisa do e-mail para LocalBusiness)."),
]
for title, sev, desc in recs:
    sev_bg = {"ALTA": C_ALTA, "MÉDIA": C_MEDIA, "BAIXA": C_BAIXA, "INFORMATIVA": HexColor("#6B7280")}[sev]
    row = Table([
        [Paragraph(f"<b>{title}</b>", ParagraphStyle('recTitle', parent=sBodySmall, fontSize=8, leading=10, textColor=C_DARK)), chip(sev, sev_bg)]
    ], colWidths=[138*mm, 22*mm])
    row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (0,0), 0)]))
    story.append(row)
    story.append(Paragraph(desc, ParagraphStyle('recDesc', parent=sBodySmall, fontSize=7.5, leading=10.5, textColor=HexColor("#374151"), leftIndent=4)))
    story.append(Spacer(1,2*mm))

# ISSUES PARA GITHUB
story.append(Paragraph("Issues para o GitHub — prontos para copiar e colar", sH1))
story.append(HRFlowable(width="100%", thickness=0.6, color=C_BORDER, spaceAfter=2, spaceBefore=0))
story.append(Paragraph(
    "Cada bloco entre <b>--- ISSUE n ---</b> e <b>--- FIM ISSUE n ---</b> é o corpo completo de uma issue em Markdown. "
    "Título no formato <i>[Segurança] …</i>, labels sugeridas e checklist de aceite verificável. Agrupamos achados triviais para evitar spam.",
    sBodySmall
))
story.append(Spacer(1,2*mm))

issues = [
    {
        "n": 1,
        "title": "[Segurança] Remover orçamentos em PDF do web root e do histórico git (exposição de pricing + PII)",
        "labels": "security, severidade:alta",
        "body": """## Descrição
Orçamentos em PDF estão versionados e dentro do document root. Qualquer deploy estático (GitHub Pages, Netlify, Vercel) os serve publicamente em `https://www.maquiadorasue.com/ORÇAMENTO%202026%20-%20DEBUTANTE.pdf.pdf`.

**Por que é explorável:** acesso direto via URL previsível, sem autenticação. Vaza tabela de preços 2026 e dado pessoal de cliente (arquivo nominal “Helena”). Histórico git preserva o arquivo mesmo após `git rm`.

## Evidência
- `git ls-files | grep pdf` (linhas do índice git):
  - `ORÇAMENTO 2026 - DEBUTANTE.pdf.pdf` (4,4 MB, tracked)
  - `Orçamento Noiva Helena 2026..pdf` (12,8 MB, tracked)
- Diretório contém ainda 22× `Shooting (n).jpeg` brutos (2–4 MB cada) — ampliam superfície de enumeration.

## Impacto
Vazamento de estratégia comercial (pricing) e PII de cliente → risco LGPD, vantagem concorrencial, phishing direcionado.

## Sugestão de correção
1. `git rm --cached "ORÇAMENTO 2026 - DEBUTANTE.pdf.pdf" "Orçamento Noiva Helena 2026..pdf"`
2. Mover PDFs para storage privado (Google Drive com link restrito / S3 privado com URL assinada) ou pasta fora do deploy (`/private` ignorada pelo host).
3. Limpar histórico: `git filter-repo --path "ORÇAMENTO 2026 - DEBUTANTE.pdf.pdf" --invert-paths` ou BFG Repo-Cleaner; force-push com coordenação.
4. Adicionar ao `.gitignore`: `*.pdf` (ou allowlist explícita) e `Shooting*.jpeg` brutos; manter só `*.webp` otimizados.
5. Se precisar expor orçamento, servir via link temporário com expiração ou endpoint com auth.
6. Configurar deploy para ignorar `/docs` e arquivos de roteiro.

## Critérios de aceite
- [ ] `git ls-files | grep -i pdf` retorna vazio (ou só PDFs publicamente intencionais)
- [ ] Acesso direto a `/ORÇAMENTO...pdf` retorna 404 no deploy de produção
- [ ] Histórico reescrito (ou ao menos PDFs removidos do HEAD + aviso de rotação de dados sensíveis)
- [ ] `.gitignore` atualizado e validado com `git check-ignore -v "teste.pdf"`
"""
    },
    {
        "n": 2,
        "title": "[Segurança] Endurecer Content-Security-Policy (remover unsafe-inline, adicionar diretivas faltantes)",
        "labels": "security, severidade:média",
        "body": """## Descrição
CSP atual usa `script-src 'self' 'unsafe-inline'` e não define `object-src`, `base-uri` nem `frame-ancestors`. `unsafe-inline` anula grande parte da proteção anti-XSS; diretivas faltantes permitem `<object>`, injeção de `<base>` e clickjacking via iframe.

**Por que é explorável:** hoje não há vetor de injeção (sem `innerHTML`/`eval`), mas qualquer evolução que reflita query string ou CMS reativa o risco. `frame-ancestors` ausente permite embutir o site em iframe malicioso sobrepondo CTA de WhatsApp.

## Evidência
- `site_maquiadora_sue.html:12` — `content="default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; ... script-src 'self' 'unsafe-inline' https://www.googletagmanager.com ..."`
- `biosite.html:10` e `site_maquiadora_sue_en.html:12` — idem
- Inline JS em `site_maquiadora_sue.html:491-656` (IIFE com `addEventListener`, lightbox, filtros) exige `unsafe-inline` hoje

## Impacto
XSS persistido/refletido futuro com execução trivial; clickjacking (Medium).

## Sugestão de correção
1. Extrair bloco `<script>` (491–656) para `site.js` externo.
2. Gerar hash: `openssl dgst -sha256 -binary site.js | openssl base64` e usar `script-src 'self' 'sha256-...' https://www.googletagmanager.com` (ou nonce por request se houver SSR).
3. CSP completa sugerida (header HTTP):
   `default-src 'self'; script-src 'self' 'sha256-...' https://www.googletagmanager.com https://www.google-analytics.com; style-src 'self' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https://www.maquiadorasue.com; connect-src 'self' https://www.google-analytics.com https://analytics.google.com; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self' https://wa.me https://api.whatsapp.com; upgrade-insecure-requests`
4. Testar em `Content-Security-Policy-Report-Only` + `report-uri` antes de bloquear.

## Critérios de aceite
- [ ] Nenhum `script-src` contém `'unsafe-inline'` no header/meta final
- [ ] `object-src 'none'`, `base-uri 'self'` e `frame-ancestors 'self'` presentes
- [ ] Site carrega sem erros de CSP no console (Chrome DevTools > Issues)
- [ ] Lightbox/filtros/menu continuam funcionais sem inline JS
"""
    },
    {
        "n": 3,
        "title": "[Segurança] Servir headers de segurança via HTTP (HSTS, X-Frame-Options, Permissions-Policy)",
        "labels": "security, severidade:média",
        "body": """## Descrição
Segurança depende só de `<meta http-equiv>` (CSP, nosniff, referrer). `<meta>` não implementa HSTS e tem precedência menor que header HTTP; sem `X-Frame-Options`/`frame-ancestors` via HTTP, clickjacking permanece possível conforme host.

## Evidência
- `site_maquiadora_sue.html:13-14` — `<meta http-equiv="X-Content-Type-Options" content="nosniff">` + CSP via meta
- Ausência de `Strict-Transport-Security`, `X-Frame-Options`, `Permissions-Policy` em qualquer config (sem `_headers`, `vercel.json`, `.htaccess` no repo)

## Impacto
Clickjacking (iframe invisível sobre CTA), downgrade HTTP, permissões excessivas de browser (camera/mic/geolocation herdadas).

## Sugestão de correção
Criar config por host:
- **Netlify** → `/_headers`:
  ```
  /*
    Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
    X-Frame-Options: SAMEORIGIN
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
    Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
    Content-Security-Policy: <ver issue #2>
  ```
- **Vercel** → `vercel.json` → `headers` array equivalente
- **S3/CloudFront** → Response Headers Policy
Após migrar CSP para header, remover `<meta http-equiv="Content-Security-Policy">`.

## Critérios de aceite
- [ ] `curl -I https://www.maquiadorasue.com/` retorna `strict-transport-security`, `x-frame-options` (ou `content-security-policy` com `frame-ancestors`), `permissions-policy`
- [ ] `https://observatory.mozilla.org` ou `securityheaders.com` sobe de D para B+ ou superior
- [ ] Teste manual: site não é iframável em `https://example.com` com `<iframe src="https://www.maquiadorasue.com">` (bloqueado)
"""
    },
    {
        "n": 4,
        "title": "[Segurança] Higiene de PII e supply-chain: e-mail/telefone, Google Fonts e placeholders (baixo risco)",
        "labels": "security, severidade:baixa",
        "body": """## Descrição
Agrupado (baixo risco, mesma sprint de hardening):
1. E-mail/telefone em plain text no HTML e JSON-LD facilitam scraping/spam/BEC.
2. Google Fonts carregado de CDN sem SRI + `media=\"print\" onload` trick.
3. `Referrer-Policy: origin-when-cross-origin` vaza path/query para CDNs/redes sociais.
4. Placeholders comentados `G-XXXXXXXXXX` / `CÓDIGO_AQUI` — inofensivos hoje, mas viram vetor de hijack se ativados sem cuidado.
5. Arquivos pesados (`Shooting (n).jpeg` 2–4 MB) e `gemini-code-*.html` vazio no repo.

## Evidência
- `site_maquiadora_sue.html:49` — `"email": "suelimamakeup@gmail.com"` + `site_maquiadora_sue.html:461` — `<a href="mailto:suelimamakeup@gmail.com">` (8× `wa.me/5521995421808`)
- `site_maquiadora_sue.html:98-99` — `<link href="https://fonts.googleapis.com/css2?...\" media=\"print\" onload=\"this.media='all'\">` sem `integrity`
- `site_maquiadora_sue.html:14` — `Referrer-Policy: origin-when-cross-origin`
- `site_maquiadora_sue.html:17-18,84-93` — `<!-- G-XXXXXXXXXX -->`
- `Get-ChildItem` — 22× `Shooting (n).jpeg`, `gemini-code-1783942303074.html` (0 bytes)

## Impacto
Spam/phishing de marca (baixo), supply-chain teórico de fonts (baixo), vazamento de URL (baixo), hijack futuro de Analytics (informativo).

## Sugestão de correção
1. **PII:** se spam aumentar, trocar `mailto:` por Formspree/Netlify Forms ou ofuscar via `data-email` + JS decode; manter JSON-LD se SEO exigir.
2. **Fonts:** self-host Lato/Playfair em `/fonts` (já feito para FontAwesome) com `font-display: swap`; remover CDN ou manter com `preconnect`.
3. **Referrer:** trocar para `strict-origin-when-cross-origin` (ou `strict-origin`).
4. **Placeholders:** ao ativar GA4/GSC, remover comentário placeholder e validar propriedade com DNS ou meta com token real restrito.
5. **Higiene:** `.gitignore` → `Shooting*.jpeg`, `gemini-*.html`, `*.bak`; manter só `*.webp` otimizados no deploy.

## Critérios de aceite
- [ ] `Referrer-Policy` é `strict-origin-when-cross-origin` (ou mais restritiva) em header/meta
- [ ] Google Fonts self-hosted OU decisão documentada de manter CDN com risco aceito
- [ ] `mailto:` permanece só se decisão de negócio registrada; caso ofuscado, `curl` não extrai e-mail em plain text
- [ ] `.gitignore` cobre `Shooting*.jpeg` e `gemini-*.html`; `git ls-files` não lista mais brutos
"""
    },
]

for iss in issues:
    story.append(Paragraph(f"--- ISSUE {iss['n']} ---", ParagraphStyle('issueDelim', parent=sBodySmall, fontSize=7, leading=9, textColor=HexColor("#92400E"), alignment=TA_CENTER, backColor=HexColor("#FFFBEB"), borderPadding=(3,3,3))))
    story.append(Spacer(1,2*mm))
    # Title block
    title_data = [[Paragraph(f"<b>{iss['title']}</b>", ParagraphStyle('issTitle', parent=sBodySmall, fontSize=8.5, leading=11, textColor=C_DARK)), Paragraph(f"<font color=\"#6B7280\" size=6>Labels: {iss['labels']}</font>", ParagraphStyle('issLabels', parent=sBodySmall, alignment=TA_CENTER))]]
    # Actually simpler: title + labels row
    story.append(Paragraph(f"<b>{iss['title']}</b>", ParagraphStyle('issT', parent=sBody, fontSize=9, leading=12, textColor=C_DARK, backColor=HexColor("#FFFBEB"), borderPadding=(4,4,4))))
    story.append(Paragraph(f"<font color=\"#6B7280\"><b>Labels sugeridas:</b> {iss['labels']}</font>", sBodySmall))
    story.append(Spacer(1,2*mm))
    # Body as mono-like but with markdown preserved: use preformatted
    # Use Paragraph with white-space preserved via <br/> conversion
    body_html = iss['body'].replace('\n', '<br/>').replace('**', '<b>').replace('**', '</b>')  # simple
    # Better: keep as preformatted with font Courier and allow markdown readability - we'll use Paragraph with smaller font and preserve line breaks
    # We'll split by lines and join with <br/>
    import html as htmlmod
    # Escape and then convert markdown-like ** to bold already above is naive, so instead render raw with HTML escaping for < > but keep ** as is for markdown copy-paste expectation: we want raw markdown inside code-like block
    raw = iss['body']
    # Use a table with one cell containing preformatted text in Courier
    pre_style = ParagraphStyle('pre', parent=styles['Normal'], fontSize=6.6, leading=9, textColor=HexColor("#1F2937"), fontName='Courier', alignment=TA_LEFT, wordWrap='CJK')
    # Need to escape HTML entities but preserve markdown
    escaped = htmlmod.escape(raw).replace('\n', '<br/>')
    # Fix double escaping for htmlmod? We'll just use Paragraph with escaped
    story.append(Table([[Paragraph(escaped, pre_style)]], colWidths=[170*mm], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#F9FAFB")),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#E5E7EB")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ])))
    story.append(Spacer(1,1*mm))
    story.append(Paragraph(f"--- FIM ISSUE {iss['n']} ---", ParagraphStyle('issueDelim2', parent=sBodySmall, fontSize=7, leading=9, textColor=HexColor("#92400E"), alignment=TA_CENTER, backColor=HexColor("#FFFBEB"), borderPadding=(3,3,3))))
    story.append(Spacer(1,4*mm))

# Apêndice: cobertura
story.append(Paragraph("Apêndice — cobertura da auditoria", sH2))
story.append(Paragraph(
    "Arquivos inspecionados <b>linha-a-linha</b>: <i>site_maquiadora_sue.html</i> (659 linhas), <i>site_maquiadora_sue_en.html</i> (676 linhas), <i>biosite.html</i> (110 linhas), "
    "<i>shared.css</i> (123 linhas), <i>site.css</i> (462 linhas), <i>biosite.css</i> (96 linhas), <i>fontawesome.css</i>, <i>record_site.js</i> (134 linhas), <i>.gitignore</i>, <i>.vscode/launch.json</i>, histórico git (5 commits, <i>git log --patch</i>), índice git (<i>git ls-files</i>). "
    "Grep global executado para: <i>innerHTML|outerHTML|dangerously|v-html|eval(|new Function|javascript:|insertAdjacentHTML|document.write</i> → 0 hits; "
    "<i>api_key|secret|password|token|AKIA|ghp_|sk-|BEGIN PRIVATE</i> → 0 hits; <i>isAdmin|canEdit|role</i> → 0 hits; <i>fetch|XMLHttpRequest|axios</i> → 0 hits. "
    "Validação cruzada: toda ocorrência de <i>target=\"_blank\"</i> (21) verificada quanto a <i>rel=noopener</i>; todo <i>script-src</i> e <i>integrity</i> conferidos.",
    sBodySmall
))
story.append(Spacer(1,2*mm))
story.append(Paragraph(
    "Limitações: auditoria estática sem execução de servidor; headers HTTP reais não observáveis sem deploy — recomendações P3 baseiam-se em ausência de config no repo e devem ser validadas com <i>curl -I</i> em produção.",
    ParagraphStyle('limit', parent=sBodySmall, fontSize=6.5, leading=8, textColor=HexColor("#6B7280"), borderPadding=(4,4,4), backColor=HexColor("#F9FAFB"))
))

# Build
doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=30*mm, bottomMargin=16*mm,
    title="Relatório de Auditoria de Segurança — Maquiadora Sue",
    author="Muse Spark",
    subject="Auditoria de segurança — site estático",
    keywords="segurança, audit, CSP, XSS, PII, static site",
)

# Need to handle first page without header
def first_page(canvas, doc):
    cover_footer(canvas, doc)

def later_pages(canvas, doc):
    header_footer(canvas, doc)

# We need to set page templates: easiest is to build with custom onFirstPage/onLaterPages
doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"PDF gerado: {OUT_PDF} ({OUT_PDF.stat().st_size/1024:.1f} KB)")
