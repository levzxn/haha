import pdfplumber
from reportlab.platypus import BaseDocTemplate, Paragraph, Spacer, Table, TableStyle,Frame,PageTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4

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
    elif '\t' in text or text.count(' ') > len(text) // 3:  # Heurística para tabelas
        return "Tabela"
    else:
        return "Parágrafo"


def extract_and_classify_content_from_pdf(pdf_path):
    """
    Extrai e classifica o conteúdo de um PDF em Título, Parágrafo, Tabela e Lista.

    Args:
        pdf_path (str): Caminho para o arquivo PDF.

    Returns:
        list: Lista de dicionários com o conteúdo classificado.
    """
    classified_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Processa cada parágrafo
                paragraphs = text.split('\n')
                for paragraph in paragraphs:
                    classification = classify_paragraph(paragraph)
                    classified_content.append({
                        'content': paragraph,
                        'type': classification
                    })

            # Extrair tabelas
            tables = page.extract_tables()
            for table in tables:
                classified_content.append({
                    'content': table,
                    'type': 'Tabela'
                })

    return classified_content

def create_pdf(pdf_paths, output_pdf):
    """
    Cria um PDF a partir de conteúdo classificado de múltiplos PDFs.

    Args:
        pdf_paths (list): Lista de caminhos para os arquivos PDF.
        output_pdf (str): Caminho para o arquivo PDF de saída.
    """
    doc = BaseDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    
    width, height = A4
    margin = 50
    column_width = (width - 2 * margin) / 2
    column_heigth = height - 2 * margin
    frame1 = Frame(margin, margin, column_width,column_heigth , id='col1')
    frame2 = Frame(margin+column_width, margin, column_width,column_heigth , id='col1')


    # Adicionar as duas colunas em cada página
    template = PageTemplate(id='TwoCol', frames=[frame1, frame2])
    doc.addPageTemplates([template])

    # Definir estilos
    title_style = ParagraphStyle(
        'TitleStyle',
        fontSize=16,
        leading=20,
        spaceAfter=12,
        alignment=1,  # Centralizado
        fontName="Helvetica-Bold"
    )

    normal_style = styles["Normal"]

    list_style = ParagraphStyle(
        'ListStyle',
        leftIndent=20,
        spaceAfter=6
    )

    story = []


    for pdf_path in pdf_paths:
        classified_content = extract_and_classify_content_from_pdf(pdf_path)

        # Adicionar conteúdo classificado ao documento final
        for item in classified_content:
            if item['type'] == 'Título':
                story.append(Paragraph(item['content'], title_style))
            elif item['type'] == 'Parágrafo':
                story.append(Paragraph(item['content'], normal_style))
            elif item['type'] == 'Lista':
                story.append(Paragraph(item['content'], list_style))
            elif item['type'] == 'Tabela':
                table_data = item['content']
                if table_data:
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)

            story.append(Spacer(1, 12))  # Espaçamento após cada elemento

    # Criar o documento PDF final
    doc.build(story)



