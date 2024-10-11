from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Table, TableStyle, Frame, PageTemplate, Spacer, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import docx

def extract_paragraphs_from_docx(docx_file):
    doc = docx.Document(docx_file)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return paragraphs

pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

def create_pdf(pdf_paths, output_pdf):
    doc = BaseDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()

    width, height = A4
    margin = 50
    column_width = (width - 2 * margin) / 2
    column_height = height - 2 * margin
    frame1 = Frame(margin, margin, column_width, column_height, id='col1')
    frame2 = Frame(margin + column_width, margin, column_width, column_height, id='col2')

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    title_style = ParagraphStyle(
        'TitleStyle',
        fontName="Calibri",
        fontSize=11,
        leading=14,
        spaceAfter=0,
        alignment=TA_CENTER  
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        fontName="Calibri",
        fontSize=9,
        leading=10.8,
        alignment=TA_JUSTIFY
        
    )

    list_style = ParagraphStyle(
        'ListStyle',
        fontName="Calibri",
        fontSize=9,
        leftIndent=20,
        spaceAfter=6,
        bulletText='- ',
    )

    table_text_style = ParagraphStyle(
        'TableTextStyle',
        fontName="Calibri",
        fontSize=9,
        leading=10.8,
    )

    story = []

    # Processar cada PDF e gerar o conteúdo classificado
    for pdf_path in pdf_paths:
        docx_file = 'documento_exemplo.docx'  # O caminho para o seu arquivo DOCX
        paragraphs = extract_paragraphs_from_docx(pdf_path)
        for paragraph in paragraphs:
            if len(paragraph) <=50:
                story.append(Paragraph(paragraph,title_style))
            else:
                story.append(Paragraph(paragraph, normal_style))
            story.append(Spacer(1, 10))

    doc.build(story)


