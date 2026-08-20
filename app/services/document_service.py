from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text(
    filename: str,
    content: bytes,
) -> str:

    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        return extract_txt(content)

    if extension == ".pdf":
        return extract_pdf(content)

    if extension == ".docx":
        return extract_docx(content)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def extract_txt(content: bytes) -> str:

    try:
        return content.decode("utf-8")

    except UnicodeDecodeError:
        return content.decode(
            "latin-1",
            errors="replace",
        )


def extract_pdf(content: bytes) -> str:

    reader = PdfReader(
        BytesIO(content)
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def extract_docx(content: bytes) -> str:

    document = Document(
        BytesIO(content)
    )

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)