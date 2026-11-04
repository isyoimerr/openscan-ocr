from pathlib import Path

import pytest
from PIL import Image

from openscan.documents import DocumentError, load_pages
from openscan.preprocessing import preprocess_image

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def test_load_image():
    path = EXAMPLES / "factura_01_limpia.png"
    pages = load_pages(path.name, path.read_bytes())
    assert len(pages) == 1
    assert pages[0].image.mode == "RGB"
    assert pages[0].page_number == 1


def test_load_image_only_pdf():
    path = EXAMPLES / "facturas_demo_3paginas.pdf"
    pages = load_pages(path.name, path.read_bytes())
    assert len(pages) == 3
    assert all(p.image.width > 500 for p in pages)


def test_pdf_page_limit_is_enforced():
    path = EXAMPLES / "facturas_demo_3paginas.pdf"
    with pytest.raises(DocumentError, match="limite"):
        load_pages(path.name, path.read_bytes(), max_pages=2)


def test_reject_invalid_file():
    with pytest.raises(DocumentError, match="Formato"):
        load_pages("malware.exe", b"abc")
    with pytest.raises(DocumentError, match="vacio"):
        load_pages("blank.png", b"")


def test_preprocess_all_modes():
    image = Image.new("RGB", (128, 128), "white")
    for mode in ("original", "grayscale", "otsu", "adaptive"):
        prepared = preprocess_image(image, mode)
        assert prepared.size == (128, 128)
        assert prepared.mode in {"RGB", "L"}


def test_oversized_image_rejected():
    from io import BytesIO
    from PIL import Image

    image = Image.new("RGB", (4000, 4000), "white")
    output = BytesIO()
    image.save(output, format="PNG")
    with pytest.raises(DocumentError, match="demasiado grande"):
        load_pages("muy_grande.png", output.getvalue())


def test_oversized_pdf_page_rejected_before_render():
    from io import BytesIO
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=9000, height=9000)
    output = BytesIO()
    writer.write(output)
    with pytest.raises(DocumentError, match="demasiado grande"):
        load_pages("gigante.pdf", output.getvalue())
