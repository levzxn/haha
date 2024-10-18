from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import docx

def header_template(canvas, doc):
    width, height = A4

    canvas.saveState()

    # Ajuste para o título principal com fonte maior e negrito
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(width / 2.0, height - 2.5 * cm, "DIÁRIO OFICIAL ELETRÔNICO")

    # Subtítulo
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(width / 2.0, height - 3.2 * cm, "DO MUNICÍPIO DE PEDRO AFONSO - TO")

    # Linha horizontal
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(1)
    canvas.line(2 * cm, height - 3.7 * cm, width - 2 * cm, height - 3.7 * cm)

    # Texto adicional
    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(width / 2.0, height - 4.2 * cm, "LEI MUNICIPAL N° 42 DE 11 DE JUNHO DE 2021")

    # Informações de data
    canvas.drawCentredString(width / 2.0, height - 5 * cm, "ANO IV - PEDRO AFONSO, TERÇA - FEIRA, 15 DE OUTUBRO DE 2024 - Nº 661")

    canvas.restoreState()

def extract_paragraphs_from_docx(docx_file):
    doc = docx.Document(docx_file)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return paragraphs

pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

def create_pdf(doc_paths, output_pdf):
    doc = BaseDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()

    width, height = A4
    margin = 1 * cm
    column_width = (width - 2 * margin) / 2
    usable_height = height - 2 * margin
    header_height = 5 * cm  

    frame1_first = Frame(
        margin,
        margin, 
        column_width,
        usable_height - header_height,
        id='col1_first',

    )
    frame2_first = Frame(
        margin + column_width,
        margin,
        column_width,
        usable_height - header_height,
        id='col2_first'
    )

    frame1_later = Frame(
        margin,
        margin,
        column_width,
        usable_height,  
        id='col1_later'
    )
    frame2_later = Frame(
        margin + column_width,
        margin,
        column_width,
        usable_height,
        id='col2_later',
    )

    first_page_template = PageTemplate(
        id='FirstPage',
        frames=[frame1_first, frame2_first],
        onPage=header_template,
        autoNextPageTemplate='LaterPages'  
    )

    later_page_template = PageTemplate(
        id='LaterPages',
        frames=[frame1_later, frame2_later],
        autoNextPageTemplate='LaterPages'
    )

    doc.addPageTemplates([first_page_template, later_page_template])

    title_style = ParagraphStyle(
        'TitleStyle',
        fontName="Calibri",
        fontSize=8,
        leading=14,
        spaceAfter=0,
        alignment=TA_CENTER
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        fontName="Calibri",
        fontSize=8,
        leading=10.8,
        alignment=TA_JUSTIFY
    )

    story = []

    for doc_path in doc_paths:
        paragraphs = extract_paragraphs_from_docx(doc_path)
        for paragraph in paragraphs:
            if len(paragraph) <= 50:
                story.append(Paragraph(paragraph, title_style))
            else:
                story.append(Paragraph(paragraph, normal_style))
            story.append(Spacer(1, 10))

    doc.build(story)