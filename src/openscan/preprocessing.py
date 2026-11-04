"""Image preparation strategies for OCR experiments and production use."""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image

PREPROCESS_MODES = {
    "original": "Sin binarizar (original)",
    "grayscale": "Escala de grises",
    "otsu": "Binarizacion Otsu",
    "adaptive": "Binarizacion adaptativa",
}


def preprocess_image(image: Image.Image, mode: str = "original") -> Image.Image:
    """Transform an image without mutating the input."""
    if mode not in PREPROCESS_MODES:
        raise ValueError(f"Modo de preprocesamiento no reconocido: {mode}")
    if mode == "original":
        return image.convert("RGB")

    gray = np.asarray(image.convert("L"))
    if mode == "grayscale":
        return Image.fromarray(gray.copy())

    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    if mode == "otsu":
        _, result = cv2.threshold(
            denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:
        result = cv2.adaptiveThreshold(
            denoised,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            11,
        )
    return Image.fromarray(result)
