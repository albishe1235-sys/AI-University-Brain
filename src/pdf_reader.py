
from pypdf import PdfReader

def read_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        pages.append({
            "page_number": page_number,
            "content": text
        })

    return pages
