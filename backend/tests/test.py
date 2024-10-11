import pdfplumber

def inspect_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"--- Página {i + 1} ---")
                print(text)
                print("\n" + "="*50 + "\n")
inspect_pdf_text('C:/Users/lucas/Documents/GitHub/login-fastapi-nextjs/backend/fast_zero/uploads/22 - Portaria (2).pdf')

print('teste da branch')