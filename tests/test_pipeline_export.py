from io import BytesIO
from pathlib import Path
import zipfile

from pypdf import PdfReader

from openscan.documents import load_pages
from openscan.export import images_to_searchable_pdf, rows_to_csv, safe_stem, texts_to_zip
from openscan.pipeline import process_page, process_pages

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


def test_process_page_reports_timeout_as_failed(monkeypatch):
    sample = EXAMPLES / "factura_01_limpia.png"
    page = load_pages(sample.name, sample.read_bytes())[0]

    def fake_run_tesseract(*args, **kwargs):
        raise TimeoutError("Tesseract process timeout")

    monkeypatch.setattr("openscan.pipeline.run_tesseract", fake_run_tesseract)

    row, result = process_page(page, reference="FACTURA", lang="spa", psm=6)
    assert row["status"] == "failed"
    assert row["cer"] is None
    assert row["wer"] is None
    assert result.text == ""
    assert "timeout" in row["error"].lower()


def test_process_pages_summary_counts_partial_success(monkeypatch):
    sample = EXAMPLES / "factura_01_limpia.png"
    pages = load_pages(sample.name, sample.read_bytes())

    def fake_process_page(page, **kwargs):
        if page.page_number == 1:
            return {
                "archivo": page.source_name,
                "pagina": page.page_number,
                "motor": "Tesseract",
                "modelo": "tesseract-psm-6",
                "preprocesamiento": kwargs["preprocessing"],
                "psm": kwargs["psm"],
                "idioma": kwargs["lang"],
                "caracteres": 7,
                "palabras": 1,
                "tiempo_segundos": 0.2,
                "cer": None,
                "wer": None,
                "tokens_entrada": 0,
                "tokens_salida": 0,
                "status": "success",
            }, type("Result", (), {"text": "FACTURA", "engine": "Tesseract", "seconds": 0.2, "model": "tesseract-psm-6", "input_tokens": 0, "output_tokens": 0})()
        raise TimeoutError("Tesseract process timeout")

    monkeypatch.setattr("openscan.pipeline.process_page", fake_process_page)
    summary = process_pages(pages, engine="Tesseract", lang="spa", psm=6, preprocessing="original")
    assert summary["attempted"] == 1
    assert summary["completed"] == 1
    assert summary["failed"] == 0
    assert len(summary["entries"]) == 1


def test_searchable_pdf_contains_text():
    sample = EXAMPLES / "factura_01_limpia.png"
    page = load_pages(sample.name, sample.read_bytes())[0]
    blob = images_to_searchable_pdf([page.image], lang="spa", psm=6)
    reader = PdfReader(BytesIO(blob))
    assert len(reader.pages) == 1
    assert "FACTURA" in (reader.pages[0].extract_text() or "")
