from io import BytesIO
from pathlib import Path
import zipfile

from pypdf import PdfReader

from openscan.documents import load_pages
from openscan.export import images_to_searchable_pdf, rows_to_csv, safe_stem, texts_to_zip
from openscan.pipeline import process_page

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def test_tesseract_pipeline_with_reference():
    sample = EXAMPLES / "factura_01_limpia.png"
    truth = (EXAMPLES / "factura_referencia.txt").read_text(encoding="utf-8")
    page = load_pages(sample.name, sample.read_bytes())[0]
    row, result = process_page(page, reference=truth, lang="spa", psm=6)
    assert "FACTURA" in result.text
    assert row["cer"] is not None
    assert row["cer"] < 0.1
    assert row["motor"] == "Tesseract"


def test_export_csv_and_zip():
    csv_bytes = rows_to_csv([{"archivo": "demo.pdf", "pagina": 1, "motor": "Tesseract"}])
    assert "demo.pdf" in csv_bytes.decode("utf-8-sig")
    zip_bytes = texts_to_zip([("../../danger.pdf", 1, "Tesseract", "texto")])
    with zipfile.ZipFile(BytesIO(zip_bytes)) as archive:
        assert len(archive.namelist()) == 1
        assert ".." not in archive.namelist()[0]
        assert archive.read(archive.namelist()[0]).decode() == "texto"
    assert safe_stem("example.pdf") == "example"


def test_searchable_pdf_contains_text():
    sample = EXAMPLES / "factura_01_limpia.png"
    page = load_pages(sample.name, sample.read_bytes())[0]
    blob = images_to_searchable_pdf([page.image], lang="spa", psm=6)
    reader = PdfReader(BytesIO(blob))
    assert len(reader.pages) == 1
    assert "FACTURA" in (reader.pages[0].extract_text() or "")
