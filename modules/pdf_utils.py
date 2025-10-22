import io
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def extract_text_from_pdf(uploaded_file):
    """Extracts text from each page and returns a list of page texts."""
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())
    return pages


def create_pdf_from_pages(page_texts, output_path):
    """Creates a PDF preserving page structure (one corrected text per page)."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4

    for page_text in page_texts:
        y = height - 60
        for line in page_text.split("\n"):
            if y < 60:  # prevent overflow (just in case)
                can.showPage()
                y = height - 60
            can.drawString(50, y, line[:100])  # limit long lines
            y -= 15
        can.showPage()

    can.save()

    with open(output_path, "wb") as f:
        f.write(packet.getvalue())
