"""Reproduce the public synthetic-image Tesseract benchmark.

Run from repository root:
    python research/run_benchmark.py

No external API, secrets or private documents are required.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import pandas as pd
import pytesseract

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from openscan.documents import load_pages  # noqa: E402
from openscan.pipeline import process_page  # noqa: E402

EXAMPLES = ROOT / "examples"
IMAGES = [
    "factura_01_limpia.png",
    "factura_02_inclinada.png",
    "factura_03_ruido.png",
]
METHODS = ["original", "otsu", "adaptive"]
PSMS = [4, 6, 11]


def main() -> None:
    truth = (EXAMPLES / "factura_referencia.txt").read_text(encoding="utf-8")
    rows = []
    for filename in IMAGES:
        blob = (EXAMPLES / filename).read_bytes()
        page = load_pages(filename, blob)[0]
        for method in METHODS:
            for psm in PSMS:
                row, _ = process_page(
                    page,
                    engine="Tesseract",
                    preprocessing=method,
                    psm=psm,
                    lang="spa",
                    reference=truth,
                )
                row["sha256_imagen"] = hashlib.sha256(blob).hexdigest()
                row["tesseract_version"] = str(pytesseract.get_tesseract_version()).split()[0]
                rows.append(row)
                print(f"{filename} | {method:8} | PSM {psm:2} | CER {row['cer']:.4f}")

    frame = pd.DataFrame(rows)
    output = ROOT / "research" / "resultados_tesseract.csv"
    frame.to_csv(output, index=False, encoding="utf-8")
    print("\nCER por preprocesamiento (promedio de todas las pruebas):")
    print(frame.groupby("preprocesamiento")["cer"].mean().round(4))
    print("\nCER por PSM (promedio de todas las pruebas):")
    print(frame.groupby("psm")["cer"].mean().round(4))
    print("\nGuardado:", output)


if __name__ == "__main__":
    main()
