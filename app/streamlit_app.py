"""OpenScan OCR web interface. Run: streamlit run app/streamlit_app.py"""

from __future__ import annotations

import os
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# Support running directly from a source checkout, without pip install -e .
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from openscan.documents import DocumentError, load_pages  # noqa: E402
from openscan.engines import (  # noqa: E402
    GEMINI_DEFAULT_MODEL,
    available_tesseract_languages,
)
from openscan.export import (  # noqa: E402
    images_to_searchable_pdf,
    rows_to_csv,
    texts_to_zip,
)
from openscan.pipeline import process_page  # noqa: E402
from openscan.preprocessing import PREPROCESS_MODES  # noqa: E402

st.set_page_config(
    page_title="OpenScan OCR | Documentos a texto",
    page_icon="\U0001f4c4",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1220px; padding-top: 2rem;}
    [data-testid="stMetric"] {padding: 14px 18px; border: 1px solid #263B4D;
         border-radius: 12px; background: #111E2E;}
    .hero {background: linear-gradient(110deg, #11273B 0%, #132233 60%, #0C2530 100%);
           border: 1px solid #294358; padding: 28px 32px; border-radius: 18px;
           margin-bottom: 24px;}
    .hero h1 {font-size: 2.5rem; margin-bottom: 5px; letter-spacing: -0.055em;}
    .hero p {font-size: 1rem; color: #B7CDD8; margin: 0; max-width: 730px;}
    .eyebrow {color: #3AD9C3; letter-spacing: 0.14em; text-transform: uppercase;
              font-size: 0.72rem; font-weight: 700; margin-bottom: 9px;}
    </style>
    <div class="hero">
      <div class="eyebrow">OPEN SOURCE &nbsp; / &nbsp; OCR TOOLKIT</div>
      <h1>OpenScan OCR</h1>
      <p>Convierte imagenes y PDF escaneados en texto utilizable.
         Procesa documentos, compara metodos y exporta resultados.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def read_secret(name: str) -> str:
    value = os.getenv(name, "")
    if value:
        return value
    try:
        return str(st.secrets.get(name, ""))
    except Exception:
        return ""


# Public deployments default to Tesseract-only. The host operator must opt in
# explicitly before server-owned API credentials can be used by anonymous users.
cloud_enabled = os.getenv("OPENSCAN_ENABLE_CLOUD", "false").lower() in {"1", "true", "yes"}
api_key = read_secret("GEMINI_API_KEY") if cloud_enabled else ""
gemini_model = read_secret("GEMINI_MODEL") or GEMINI_DEFAULT_MODEL

MAX_FILES = 4
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 20 * 1024 * 1024
MAX_TOTAL_PAGES = 5

try:
    languages = available_tesseract_languages()
except Exception:
    languages = []

if not languages:
    st.error(
        "Tesseract no esta disponible. Instala el programa y el idioma espanol: "
        "consulta docs/INSTALL.md."
    )
    st.stop()

st.sidebar.header("Configuracion")
st.sidebar.caption("Tesseract se ejecuta en el servidor de Render; no en tu dispositivo.")

engine_options = ["Tesseract (local en el servidor)"]
if api_key:
    engine_options += ["Gemini (nube)", "Comparar ambos"]
engine_selection = st.sidebar.radio("Motor OCR", engine_options, index=0)
preprocessing = st.sidebar.selectbox(
    "Tratamiento de imagen",
    list(PREPROCESS_MODES),
    format_func=lambda mode: PREPROCESS_MODES[mode],
)
psm = st.sidebar.selectbox("PSM de Tesseract", [6, 4, 11, 3], index=0)
language = st.sidebar.selectbox(
    "Idioma Tesseract",
    languages,
    index=(languages.index("spa") if "spa" in languages else 0),
)
max_pages = st.sidebar.slider("Maximo de paginas por PDF", min_value=1, max_value=5, value=3)

if not cloud_enabled:
    st.sidebar.info("La demo publica utiliza Tesseract. Gemini esta desactivado por defecto.")
elif not api_key:
    st.sidebar.info("Gemini requiere GEMINI_API_KEY configurada por el administrador.")
else:
    st.sidebar.success(f"Gemini disponible: {gemini_model}")

st.sidebar.divider()
st.sidebar.caption(
    "Los archivos se procesan en la memoria del servidor y se conservan durante "
    "la sesion. No hay almacenamiento permanente configurado. "
    "No subas documentos personales, financieros, medicos ni confidenciales."
)
st.sidebar.markdown("[Codigo en GitHub](https://github.com/isyoimerr/openscan-ocr)")

col_upload, col_info = st.columns([1.65, 1], gap="large")
with col_upload:
    st.subheader("1. Carga documentos")
    uploads = st.file_uploader(
        "Imagenes o PDF escaneados",
        type=["png", "jpg", "jpeg", "webp", "pdf"],
        accept_multiple_files=True,
        help="Maximo 4 archivos, 10 MB por archivo y 5 paginas en total por ejecucion.",
    )
    reference = st.text_area(
        "Texto correcto de referencia (opcional)",
        height=95,
        placeholder="Si procesas una sola pagina, pega aqui el texto real para calcular CER y WER.",
    )
    st.caption(
        "Demo publica: usa solamente archivos de prueba o documentos que puedas compartir. "
        "El OCR se ejecuta en el servidor del proyecto, no en tu dispositivo."
    )
    if engine_selection != "Tesseract (local en el servidor)":
        st.warning(
            "Gemini envia las imagenes a la API externa de Google. "
            "No lo utilices con documentos privados sin autorizacion."
        )
    start = st.button(
        "Procesar documentos", type="primary", use_container_width=True,
        disabled=not bool(uploads),
    )

with col_info:
    st.subheader("Que puedes hacer")
    st.markdown(
        """
        **01** - Extraer texto de fotografias y PDF sin capa de texto.  
        **02** - Probar imagen original, Otsu y binarizacion adaptativa.  
        **03** - Comparar resultados y tiempos de OCR.  
        **04** - Exportar CSV, transcripciones y PDF buscable.
        """
    )
    st.caption(
        "CER y WER requieren una transcripcion de referencia. "
        "Sin ella, OpenScan no presenta una precision inventada."
    )

if start:
    if len(uploads) > MAX_FILES:
        st.error(f"Se permiten hasta {MAX_FILES} archivos por lote.")
        st.stop()
    if any(upload.size > MAX_FILE_BYTES for upload in uploads):
        st.error("Uno de los archivos supera el limite de 10 MB.")
        st.stop()
    if sum(upload.size for upload in uploads) > MAX_TOTAL_BYTES:
        st.error("El lote supera el limite total de 20 MB.")
        st.stop()
    if len(reference) > 20000:
        st.error("El texto de referencia supera 20.000 caracteres.")
        st.stop()
    all_pages = []
    problems = []
    with st.spinner("Leyendo archivos..."):
        for upload in uploads:
            try:
                pages = load_pages(
                    upload.name, upload.getvalue(), max_pages=max_pages, dpi=150
                )
                all_pages.extend(pages)
            except DocumentError as exc:
                problems.append(f"{upload.name}: {exc}")

    if len(all_pages) > MAX_TOTAL_PAGES:
        st.error("Selecciona un lote de hasta 5 paginas para evitar sobrecargar el servidor.")
    elif not all_pages:
        st.error("No fue posible leer los archivos seleccionados.")
    else:
        if reference.strip() and len(all_pages) != 1:
            st.warning(
                "La referencia textual solo se usara con una unica pagina. "
                "Se omitira para este lote."
            )
        engines = ["Tesseract"]
        if engine_selection == "Gemini (nube)":
            engines = ["Gemini"]
        elif engine_selection == "Comparar ambos":
            engines = ["Tesseract", "Gemini"]

        attempt_reference = reference.strip() if len(all_pages) == 1 and reference.strip() else None
        total_operations = len(all_pages) * len(engines)
        progress = st.progress(0, text="Extrayendo texto...")
        summary = {"rows": [], "entries": [], "failures": [], "attempted": 0, "completed": 0, "failed": 0}
        for index, page in enumerate(all_pages):
            for engine in engines:
                try:
                    row, result = process_page(
                        page,
                        engine=engine,
                        preprocessing=preprocessing,
                        lang=language,
                        psm=psm,
                        reference=attempt_reference,
                        gemini_key=api_key,
                        gemini_model=gemini_model,
                    )
                except Exception as exc:
                    summary["failures"].append({"page": page, "engine": engine, "error": str(exc)[:220]})
                    progress.progress((index * len(engines) + 1 + list(engines).index(engine)) / total_operations,
                                      text=f"Procesadas {index + 1}/{len(all_pages)} paginas ({engine})")
                    continue

                if row.get("status") == "failed":
                    summary["failures"].append({"page": page, "engine": engine, "error": row.get("error", "OCR fallido")})
                    progress.progress((index * len(engines) + 1 + list(engines).index(engine)) / total_operations,
                                      text=f"Procesadas {index + 1}/{len(all_pages)} paginas ({engine})")
                    continue

                summary["rows"].append(row)
                summary["entries"].append((page.source_name, page.page_number, engine, result.text))
                progress.progress((index * len(engines) + 1 + list(engines).index(engine)) / total_operations,
                                  text=f"Procesadas {index + 1}/{len(all_pages)} paginas ({engine})")

        summary["attempted"] = len(all_pages) * len(engines)
        summary["completed"] = len(summary["rows"])
        summary["failed"] = len(summary["failures"])
        progress.empty()
        st.session_state["openscan_report"] = {
            "rows": summary["rows"],
            "entries": summary["entries"],
            "pages": all_pages,
            "issues": problems,
            "language": language,
            "psm": psm,
            "attempted": summary["attempted"],
            "completed": summary["completed"],
            "failed": summary["failed"],
            "failures": summary["failures"],
        }
        st.session_state.pop("openscan_pdf", None)

report = st.session_state.get("openscan_report")
if report:
    st.divider()
    st.subheader("2. Resultados")
    rows = report["rows"]
    entries = report["entries"]
    pages = report["pages"]
    attempted = report.get("attempted", len(pages))
    completed = report.get("completed", len(rows))
    failed = report.get("failed", max(attempted - completed, 0))
    failures = report.get("failures", [])

    for issue in report["issues"]:
        st.warning(issue)

    if failures:
        st.warning(f"Se detectaron {failed} paginas fallidas. Las paginas con OCR correcto siguen disponibles.")
        for item in failures:
            page = item["page"]
            error = item["error"]
            st.caption(f"{page.label} / {item['engine']}: {error}")

    if rows:
        data = pd.DataFrame(rows)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Paginas intentadas", attempted)
        c2.metric("Paginas completadas", completed)
        c3.metric("Paginas fallidas", failed)
        c4.metric("Caracteres detectados", f"{data['caracteres'].sum():,}")
        if len(data) > 0:
            st.metric("Tiempo OCR total", f"{data['tiempo_segundos'].sum():.2f} s")

        tab_text, tab_metrics, tab_export = st.tabs(
            ["Texto reconocido", "Analisis y comparacion", "Descargas"]
        )
        with tab_text:
            names = [f"{name} / pagina {page} / {engine}" for name, page, engine, _ in entries]
            chosen = st.selectbox("Resultado", range(len(entries)), format_func=lambda i: names[i])
            filename, page_no, engine, text = entries[chosen]
            matching_page = next(
                p for p in pages if p.source_name == filename and p.page_number == page_no
            )
            left, right = st.columns([1, 1], gap="medium")
            with left:
                st.image(matching_page.image, caption="Documento original", use_container_width=True)
            with right:
                st.text_area("Transcripcion", value=text, height=480)
        with tab_metrics:
            st.dataframe(
                data,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "tiempo_segundos": st.column_config.NumberColumn(format="%.2f s"),
                    "cer": st.column_config.NumberColumn(format="%.4f"),
                    "wer": st.column_config.NumberColumn(format="%.4f"),
                },
            )
            if data["motor"].nunique() > 1:
                st.markdown("**Tiempo total por motor (s)**")
                timing = data.groupby("motor", as_index=True)["tiempo_segundos"].sum()
                st.bar_chart(timing)
            if data["cer"].notna().any():
                st.caption("CER y WER: 0 indica coincidencia exacta con la referencia suministrada.")
            else:
                st.caption("No hay CER ni WER porque no se proporciono texto de referencia.")
        with tab_export:
            st.markdown("**Archivos disponibles**")
            e1, e2 = st.columns(2)
            with e1:
                st.download_button(
                    "Descargar CSV",
                    data=rows_to_csv(rows),
                    file_name="openscan_resultados.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with e2:
                st.download_button(
                    "Descargar textos ZIP",
                    data=texts_to_zip(entries),
                    file_name="openscan_transcripciones.zip",
                    mime="application/zip",
                    use_container_width=True,
                )
            st.divider()
            st.markdown("**PDF buscable**")
            st.caption(
                "Crea un nuevo PDF con capa de texto usando otra pasada de Tesseract. "
                "Este paso puede fallar de forma independiente y solo debe usarse si hay paginas OCR correctas."
            )
            if st.button("Generar PDF buscable"):
                with st.spinner("Generando PDF con texto seleccionable..."):
                    try:
                        st.session_state["openscan_pdf"] = images_to_searchable_pdf(
                            [p.image for p in pages],
                            lang=report["language"],
                            psm=report["psm"],
                        )
                    except Exception as exc:
                        st.error(f"No fue posible generar el PDF: {exc}")
            if st.session_state.get("openscan_pdf"):
                st.download_button(
                    "Descargar PDF buscable",
                    data=st.session_state["openscan_pdf"],
                    file_name="openscan_buscable.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
    else:
        st.info("No se consiguieron transcripciones. Revisa las alertas anteriores.")

st.divider()
st.caption(
    "OpenScan OCR v0.1.0 | MIT | Las pruebas del repositorio usan documentos sinteticos. "
    "Revisa las transcripciones antes de usarlas en procesos importantes."
)
