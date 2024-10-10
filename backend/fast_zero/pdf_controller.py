import pdfplumber
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Table, TableStyle, Frame, PageTemplate, Spacer, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY

def classify_paragraph(text):
    """
    Classifica um parágrafo como Título, Parágrafo, Tabela ou Lista.

    Args:
        text (str): O parágrafo extraído do PDF.

    Returns:
        str: A classificação do parágrafo (Título, Parágrafo, Tabela ou Lista).
    """
    text = text.strip()

    # Regras heurísticas para classificar o texto
    if len(text) < 50 and text.isupper():
        return "Título"
    elif text.startswith('- ') or text.startswith('* ') or text[0].isdigit():
        return "Lista"
    else:
        return "Parágrafo"


def extract_and_classify_content_from_pdf(pdf_path):
    classified_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                paragraphs = text.split('\n')
                for paragraph in paragraphs:
                    classification = classify_paragraph(paragraph)
                    classified_content.append({
                        'content': paragraph,
                        'type': classification
                    })

            tables = page.extract_tables()
            for table in tables:
                classified_content.append({
                    'content': table,
                    'type': 'Tabela'
                })

    return classified_content

pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))

def create_pdf(pdf_paths, output_pdf):
    """
    Cria um PDF a partir de conteúdo classificado de múltiplos PDFs.
    """
    doc = BaseDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    
    width, height = A4
    margin = 50
    column_width = (width - 2 * margin) / 2  # Largura de metade da página
    column_height = height - 2 * margin
    frame1 = Frame(margin, margin, column_width, column_height, id='col1')
    frame2 = Frame(margin + column_width, margin, column_width, column_height, id='col2')

    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    # Definir estilos personalizados
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName="Calibri",  # Fonte Calibri
        fontSize=12,         # Exemplo de título com corpo 12
        leading=14,          # Espaçamento simples
        spaceAfter=12,
        alignment=1  # Centralizado
    )

    normal_style = ParagraphStyle(
        'NormalStyle',
        fontName="Calibri",  # Fonte Calibri
        fontSize=9,          # Corpo 9
        leading=10.8,        # Espaçamento simples (espaço simples para corpo 9)
        alignment=TA_JUSTIFY  # Justificado
    )

    list_style = ParagraphStyle(
        'ListStyle',
        fontName="Calibri",  # Fonte Calibri
        fontSize=9,
        leftIndent=20,
        spaceAfter=6,
        bulletText='- ',     # Hífen como marcador
    )

    table_text_style = ParagraphStyle(
        'TableTextStyle',
        fontName="Calibri",  # Fonte Calibri
        fontSize=9,          # Corpo 9
        leading=10.8,        # Espaçamento simples
    )

    story = []

    for pdf_path in pdf_paths:
        classified_content = extract_and_classify_content_from_pdf(pdf_path)

        for item in classified_content:
            if item['type'] == 'Título':
                story.append(Paragraph(item['content'], title_style))
            elif item['type'] == 'Parágrafo':
                story.append(Paragraph(item['content'], normal_style))
            elif item['type'] == 'Lista':
                # Utiliza hífen como marcador para listas
                list_items = [ListItem(Paragraph(line, list_style)) for line in item['content'].split("\n")]
                story.append(ListFlowable(list_items, bulletType='bullet'))
            elif item['type'] == 'Tabela':
                table_data = item['content']
                if table_data:
                    styled_table_data = [
                        [Paragraph(str(cell), table_text_style) for cell in row]
                        for row in table_data
                    ]

                    num_columns = len(table_data[0])
                    column_widths = [column_width / num_columns] * num_columns

                    table = Table(styled_table_data, colWidths=column_widths)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('LEFTPADDING', (0, 0), (-1, -1), 4),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 4)
                    ]))
                    story.append(table)

            story.append(Spacer(1, 12))

    doc.build(story)

