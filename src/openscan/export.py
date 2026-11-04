"""Export recognized text, benchmark CSVs and searchable PDFs."""

from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import csv
import re

from PIL import Image
from pypdf import PdfReader, PdfWriter
import pytesseract

CSV_FIELDS = [
    "archivo", "pagina", "motor", "modelo", "preprocesamiento", "psm",
    "idioma", "caracteres", "palabras", "tiempo_segundos", "cer", "wer",
    "tokens_entrada", "tokens_salida",
]


def rows_to_csv(rows: list[dict]) -> bytes:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def safe_stem(name: str) -> str:
    name = Path(name).stem
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_")[:70] or "archivo"


def texts_to_zip(entries: list[tuple[str, int, str, str]]) -> bytes:
    """entries: (filename, page, engine, recognized_text)."""
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for index, (filename, page, engine, text) in enumerate(entries):
            filename = f"{safe_stem(filename)}_pagina_{page}_{engine.lower()}_{index}.txt"
            archive.writestr(filename, text)
    return output.getvalue()


def images_to_searchable_pdf(
    images: list[Image.Image], *, lang: str = "spa", psm: int = 6
) -> bytes:
    """Generate a PDF with Tesseract's invisible text layer on each image."""
    if not images:
        raise ValueError("No hay paginas para exportar.")
    if psm not in {3, 4, 6, 11}:
        raise ValueError("PSM invalido.")
    writer = PdfWriter()
    for image in images:
        page_pdf = pytesseract.image_to_pdf_or_hocr(
            image.convert("RGB"),
            lang=lang,
            config=f"--oem 1 --psm {psm}",
            extension="pdf",
            timeout=45,
        )
        reader = PdfReader(BytesIO(page_pdf))
        writer.add_page(reader.pages[0])
    output = BytesIO()
    writer.write(output)
    return output.getvalue()
