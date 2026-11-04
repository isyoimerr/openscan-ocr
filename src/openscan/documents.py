"""Load image-only PDFs and raster images without writing uploaded files to disk."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError
import pypdfium2 as pdfium

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MAX_IMAGE_PIXELS = 12_000_000


class DocumentError(ValueError):
    """Raised when an uploaded document is invalid or exceeds a safety limit."""


@dataclass
class DocumentPage:
    source_name: str
    page_number: int
    image: Image.Image

    @property
    def label(self) -> str:
        return f"{self.source_name} - pagina {self.page_number}"


def _check_image_size(image: Image.Image) -> None:
    if image.width * image.height > MAX_IMAGE_PIXELS:
        raise DocumentError("Imagen demasiado grande para procesarla con seguridad.")


def load_pages(
    filename: str,
    file_bytes: bytes,
    *,
    max_pages: int = 10,
    dpi: int = 150,
) -> list[DocumentPage]:
    """Read a supported document into RGB PIL images, one per page.

    PDF pages are rasterized using PDFium. File contents are processed in memory.
    Nothing is uploaded to an external service by this function.
    """
    extension = Path(filename).suffix.lower()
    safe_name = Path(filename).name

    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentError("Formato no admitido: usa PDF, PNG, JPG o WEBP.")
    if not file_bytes:
        raise DocumentError("El archivo esta vacio.")
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise DocumentError("El archivo supera el limite de 25 MB.")
    if not 1 <= max_pages <= 30:
        raise DocumentError("El limite de paginas debe estar entre 1 y 30.")
    if not 72 <= dpi <= 250:
        raise DocumentError("DPI fuera de rango (72 a 250).")

    if extension != ".pdf":
        try:
            with Image.open(BytesIO(file_bytes)) as source:
                _check_image_size(source)
                image = ImageOps.exif_transpose(source).convert("RGB")
        except DocumentError:
            raise
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise DocumentError("No fue posible abrir la imagen.") from exc
        return [DocumentPage(safe_name, 1, image)]

    try:
        pdf = pdfium.PdfDocument(file_bytes)
    except Exception as exc:
        raise DocumentError("No fue posible abrir el PDF. Verifica que no tenga contrasena.") from exc

    pages: list[DocumentPage] = []
    try:
        total = len(pdf)
        if total == 0:
            raise DocumentError("El PDF no contiene paginas.")
        if total > max_pages:
            raise DocumentError(
                f"El PDF tiene {total} paginas y el limite seleccionado es {max_pages}."
            )
        for index in range(total):
            page = pdf[index]
            try:
                # Reject huge PDF dimensions before allocating a rendered bitmap.
                width_pt, height_pt = page.get_size()
                rendered_width = int(width_pt * dpi / 72) + 1
                rendered_height = int(height_pt * dpi / 72) + 1
                if (rendered_width <= 0 or rendered_height <= 0 or
                        rendered_width * rendered_height > MAX_IMAGE_PIXELS):
                    raise DocumentError("La pagina PDF es demasiado grande para procesarla.")
                image = page.render(scale=dpi / 72).to_pil().convert("RGB")
                _check_image_size(image)
                pages.append(DocumentPage(safe_name, index + 1, image))
            finally:
                page.close()
    except DocumentError:
        raise
    except Exception as exc:
        raise DocumentError("Error al convertir una pagina del PDF a imagen.") from exc
    finally:
        pdf.close()
    return pages
