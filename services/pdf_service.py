import PyPDF2

def extract_text_from_pdf(file_stream):
    """Extract plain text from a PDF file (uploaded via Flask)."""
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()
