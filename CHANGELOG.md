# Changelog

## [0.1.0] - 2026-11-04

Primera version publica del proyecto OpenScan OCR.

### Incluye

- Motor OCR local con Tesseract.
- Integracion opcional con Gemini (API configurada mediante secretos).
- Imagenes y PDF escaneados, con limite de paginas y tamano de carga.
- Preprocesamiento por escala de grises, Otsu y binarizacion adaptativa.
- Metricas CER, WER, tiempo y exportacion CSV.
- PDF buscable, textos ZIP y herramienta de linea de comandos.
- Aplicacion Streamlit para usuarios sin conocimientos tecnicos.
- Cuaderno publico de Colab con ejemplos ficticios.
- Benchmark reproducible de 27 combinaciones y visualizaciones.
- Pruebas automatizadas y pipeline CI.

### Limitaciones conocidas

- OCR no garantiza exactitud con documentos reales.
- La interfaz web no incluye revision humana de campos ni almacenamiento persistente.
- Gemini depende de cuotas, conectividad y disponibilidad del modelo.
