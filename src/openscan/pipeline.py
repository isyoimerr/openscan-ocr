"""Reusable OCR pipeline independent from Streamlit and Google Colab."""

from __future__ import annotations

from typing import Iterable

from .documents import DocumentPage
from .engines import GEMINI_DEFAULT_MODEL, OCRResult, run_gemini, run_tesseract
from .metrics import cer, wer
from .preprocessing import preprocess_image


def _empty_failed_row(
    page: DocumentPage,
    *,
    engine: str,
    preprocessing: str,
    lang: str,
    psm: int,
    error: Exception | str,
) -> tuple[dict, OCRResult]:
    message = str(error).strip() or "No fue posible completar la lectura OCR."
    row = {
        "archivo": page.source_name,
        "pagina": page.page_number,
        "motor": engine,
        "modelo": "",
        "preprocesamiento": preprocessing,
        "psm": psm if engine == "Tesseract" else "",
        "idioma": lang if engine == "Tesseract" else "",
        "caracteres": 0,
        "palabras": 0,
        "tiempo_segundos": 0.0,
        "cer": None,
        "wer": None,
        "tokens_entrada": 0,
        "tokens_salida": 0,
        "status": "failed",
        "error": message[:240],
    }
    return row, OCRResult(engine=engine, text="", seconds=0.0, model="", input_tokens=0, output_tokens=0)


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
    try:
        if engine == "Tesseract":
            result = run_tesseract(image, lang=lang, psm=psm)
        elif engine == "Gemini":
            result = run_gemini(image, api_key=gemini_key or "", model=gemini_model)
        else:
            raise ValueError(f"Motor OCR no reconocido: {engine}")
    except Exception as exc:
        return _empty_failed_row(page, engine=engine, preprocessing=preprocessing, lang=lang, psm=psm, error=exc)

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
        "status": "success",
    }
    return row, result


def process_pages(
    pages: Iterable[DocumentPage],
    *,
    engines: list[str] | str | None = None,
    engine: str | None = None,
    preprocessing: str = "original",
    lang: str = "spa",
    psm: int = 6,
    reference: str | None = None,
    gemini_key: str | None = None,
    gemini_model: str = GEMINI_DEFAULT_MODEL,
) -> dict:
    if engines is None:
        engines = engine or "Tesseract"
    if isinstance(engines, str):
        engines = [engines]

    rows: list[dict] = []
    entries: list[tuple[str, int, str, str]] = []
    failures: list[dict] = []
    attempted = 0

    for page in pages:
        for engine in engines:
            attempted += 1
            try:
                row, result = process_page(
                    page,
                    engine=engine,
                    preprocessing=preprocessing,
                    lang=lang,
                    psm=psm,
                    reference=reference,
                    gemini_key=gemini_key,
                    gemini_model=gemini_model,
                )
            except Exception as exc:
                failures.append({"page": page, "engine": engine, "error": str(exc)[:240]})
                continue

            if row.get("status") == "failed":
                failures.append({"page": page, "engine": engine, "error": row.get("error", "OCR fallido")})
                continue

            rows.append(row)
            entries.append((page.source_name, page.page_number, engine, result.text))

    return {
        "attempted": attempted,
        "completed": len(rows),
        "failed": len(failures),
        "rows": rows,
        "entries": entries,
        "failures": failures,
    }
