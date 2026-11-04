"""Local Tesseract and optional Google Gemini OCR engines."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import os
import shutil
import time

from PIL import Image
import pytesseract


def _resolve_tesseract_executable() -> str | None:
    env_path = os.getenv("TESSERACT_CMD")
    if env_path and os.path.exists(env_path):
        return env_path

    candidates = [
        env_path,
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    found = shutil.which("tesseract")
    return found


resolved_tesseract = _resolve_tesseract_executable()
if resolved_tesseract:
    pytesseract.pytesseract.tesseract_cmd = resolved_tesseract

GEMINI_DEFAULT_MODEL = "gemini-3.6-flash"
DEFAULT_TESSERACT_TIMEOUT = 30.0
TRANSCRIPTION_PROMPT = (
    "Transcribe exactamente el texto visible en esta imagen. "
    "Respeta numeros, signos y orden de lectura. "
    "No inventes contenido. Devuelve solo la transcripcion."
)


def tesseract_timeout_for_image(image: Image.Image, *, base_timeout: float = DEFAULT_TESSERACT_TIMEOUT) -> float:
    """Set a conservative timeout based on image size instead of a single fixed timeout."""
    pixels = max(1, image.width * image.height)
    scaled = base_timeout + max(0.0, min(20.0, pixels / 2_500_000 * 10.0))
    return max(10.0, min(35.0, scaled))


@dataclass
class OCRResult:
    engine: str
    text: str
    seconds: float
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


def available_tesseract_languages() -> list[str]:
    if not _resolve_tesseract_executable():
        return []
    try:
        return pytesseract.get_languages(config="")
    except Exception:
        return []


def run_tesseract(
    image: Image.Image,
    *,
    lang: str = "spa",
    psm: int = 6,
    timeout: float | None = None,
) -> OCRResult:
    if psm not in {3, 4, 6, 11}:
        raise ValueError("PSM admitidos: 3, 4, 6 y 11.")
    if not lang.isalpha() or len(lang) > 12:
        raise ValueError("Codigo de idioma invalido.")

    timeout_seconds = timeout if timeout is not None else tesseract_timeout_for_image(image)
    start = time.perf_counter()
    try:
        text = pytesseract.image_to_string(
            image,
            lang=lang,
            config=f"--oem 1 --psm {psm}",
            timeout=timeout_seconds,
        )
    except Exception as exc:
        detail = str(exc)
        message = detail if detail else "Tesseract process timeout"
        raise RuntimeError(message[:220]) from exc

    return OCRResult(
        engine="Tesseract",
        text=text.strip(),
        seconds=time.perf_counter() - start,
        model=f"tesseract-psm-{psm}",
    )


def run_gemini(
    image: Image.Image,
    *,
    api_key: str,
    model: str = GEMINI_DEFAULT_MODEL,
    max_attempts: int = 2,
) -> OCRResult:
    """Send a page to Gemini. Only invoked when user explicitly selects cloud OCR."""
    if not api_key:
        raise ValueError("Falta GEMINI_API_KEY. La opcion local no necesita API.")
    if not model or len(model) > 80:
        raise ValueError("Nombre del modelo Gemini invalido.")

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("Instala el extra web: pip install '.[web]'.") from exc

    buffer = BytesIO()
    image.convert("RGB").save(buffer, format="PNG")
    image_part = types.Part.from_bytes(
        data=buffer.getvalue(), mime_type="image/png"
    )
    start = time.perf_counter()
    client = genai.Client(api_key=api_key)
    try:
        last_exception: Exception | None = None
        for attempt in range(max_attempts):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[image_part, TRANSCRIPTION_PROMPT],
                )
                text = (response.text or "").strip()
                if not text:
                    raise RuntimeError("Gemini no devolvio una transcripcion.")
                metadata = getattr(response, "usage_metadata", None)
                return OCRResult(
                    engine="Gemini",
                    text=text,
                    seconds=time.perf_counter() - start,
                    model=model,
                    input_tokens=int(getattr(metadata, "prompt_token_count", 0) or 0),
                    output_tokens=int(getattr(metadata, "candidates_token_count", 0) or 0),
                )
            except Exception as exc:
                last_exception = exc
                detail = str(exc).upper()
                transient = any(code in detail for code in (
                    "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500"
                ))
                if transient and attempt + 1 < max_attempts:
                    time.sleep(2 ** attempt + 1)
                    continue
                break
        assert last_exception is not None
        message = str(last_exception).replace(api_key, "[OCULTA]")
        raise RuntimeError(
            f"No fue posible completar la llamada a Gemini: {message[:220]}"
        ) from last_exception
    finally:
        client.close()
