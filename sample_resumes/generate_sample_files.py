"""
Generates real .pdf and .docx sample resume documents for testing.
"""

import os
import docx
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(text_path, pdf_path):
    with open(text_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b")
    )
    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    elements = []
    lines = content.split("\n")
    if lines:
        elements.append(Paragraph(lines[0], title_style))
        for line in lines[1:]:
            if line.strip():
                elements.append(Paragraph(line.strip(), body_style))
            else:
                elements.append(Spacer(1, 6))

    doc.build(elements)
    print(f"Created PDF: {pdf_path}")

def generate_docx(text_path, docx_path):
    with open(text_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc = docx.Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    doc.save(docx_path)
    print(f"Created DOCX: {docx_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    samples = ["sample_ai_engineer", "sample_data_analyst", "sample_web_developer"]
    for s in samples:
        txt_file = os.path.join(base_dir, f"{s}.txt")
        if os.path.exists(txt_file):
            generate_pdf(txt_file, os.path.join(base_dir, f"{s}.pdf"))
            generate_docx(txt_file, os.path.join(base_dir, f"{s}.docx"))
