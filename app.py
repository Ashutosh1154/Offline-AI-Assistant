
from src.document_loader import load_pdf

pdf_path = "data/sample_documents/sample.pdf"

document_text = load_pdf(pdf_path)

print("PDF loaded successfully!\n")
print(document_text)

