"""Command-line interface for local OCR; no web app or API key required."""

from __future__ import annotations

import argparse
from pathlib import Path

from .documents import DocumentError, load_pages
from .export import images_to_searchable_pdf, rows_to_csv, safe_stem
from .pipeline import process_page
from .preprocessing import PREPROCESS_MODES


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="openscan-ocr",
        description="Extrae texto de un PDF o una imagen con Tesseract local.",
    )
    parser.add_argument("archivo", type=Path, help="Archivo PDF, PNG, JPG o WEBP")
    parser.add_argument("--salida", type=Path, default=Path("results_local"))
    parser.add_argument("--psm", type=int, choices=[3, 4, 6, 11], default=6)
    parser.add_argument("--pre", choices=list(PREPROCESS_MODES), default="original")
    parser.add_argument("--lang", default="spa")
    parser.add_argument("--max-paginas", type=int, default=10)
    parser.add_argument("--pdf-buscable", action="store_true")
    args = parser.parse_args(argv)

    if not args.archivo.is_file():
        parser.error(f"No se encontro el archivo: {args.archivo}")

    try:
        pages = load_pages(
            args.archivo.name, args.archivo.read_bytes(), max_pages=args.max_paginas
        )
    except DocumentError as exc:
        parser.error(str(exc))

    args.salida.mkdir(parents=True, exist_ok=True)
    rows = []
    for page in pages:
        row, result = process_page(
            page,
            preprocessing=args.pre,
            psm=args.psm,
            lang=args.lang,
        )
        rows.append(row)
        name = f"{safe_stem(args.archivo.name)}_pagina_{page.page_number}.txt"
        (args.salida / name).write_text(result.text, encoding="utf-8")
        print(f"Pagina {page.page_number} | {len(result.text)} caracteres | {result.seconds:.2f} s")

    (args.salida / "resultados.csv").write_bytes(rows_to_csv(rows))
    if args.pdf_buscable:
        pdf_bytes = images_to_searchable_pdf(
            [page.image for page in pages], lang=args.lang, psm=args.psm
        )
        (args.salida / "documento_buscable.pdf").write_bytes(pdf_bytes)
    print(f"Resultados guardados: {args.salida.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
