"""Reusable OCR pipeline independent from Streamlit and Google Colab."""

from __future__ import annotations

from .documents import DocumentPage
from .engines import GEMINI_DEFAULT_MODEL, OCRResult, run_gemini, run_tesseract
from .metrics import cer, wer
from .preprocessing import preprocess_image


def process_page(
    page: DocumentPage,
    *,
    engine: str = "Tesseract",
    preprocessing: str = "original",
    lang: str = "spa",
    psm: int = 6,
    reference: str | None = None,
    gemini_key: str | None = None,
    gemini_model: str = GEMINI_DEFAULT_MODEL,
) -> tuple[dict, OCRResult]:
    image = preprocess_image(page.image, preprocessing)
    if engine == "Tesseract":
        result = run_tesseract(image, lang=lang, psm=psm)
    elif engine == "Gemini":
        result = run_gemini(image, api_key=gemini_key or "", model=gemini_model)
    else:
        raise ValueError(f"Motor OCR no reconocido: {engine}")

    row = {
        "archivo": page.source_name,
        "pagina": page.page_number,
        "motor": result.engine,
        "modelo": result.model,
        "preprocesamiento": preprocessing,
        "psm": psm if engine == "Tesseract" else "",
        "idioma": lang if engine == "Tesseract" else "",
        "caracteres": len(result.text),
        "palabras": len(result.text.split()),
        "tiempo_segundos": round(result.seconds, 3),
        "cer": cer(reference, result.text),
        "wer": wer(reference, result.text),
        "tokens_entrada": result.input_tokens,
        "tokens_salida": result.output_tokens,
    }
    return row, result
