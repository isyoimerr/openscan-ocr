# Roadmap | OpenScan OCR

## v0.1.0 - Base abierta y prototipo funcional (actual)

- [x] Motor local reutilizable con Tesseract.
- [x] PDF escaneado e imágenes.
- [x] Preprocesamiento original / gris / Otsu / adaptativo.
- [x] CER, WER y tiempos con transcripciones de referencia.
- [x] Benchmark reproducible sobre documentos sintéticos.
- [x] Cuaderno público de Google Colab.
- [x] Interfaz web con carga de documentos y exportación.
- [x] Gemini opcional configurado por secretos.
- [x] Pruebas automatizadas y CI.

## v0.2 - Calidad y facilidad de uso

- [ ] Indicadores de confianza por palabra.
- [ ] Corrección de inclinación y rotación automática.
- [ ] Interfaz para revisar y corregir el texto reconocido.
- [ ] Exportación por documento, sin agrupar PDF distintos.
- [ ] Pruebas sobre datos adicionales con permiso o sintéticos.

## v0.3 - Documentos convertidos en datos

- [ ] Extracción configurable de campos de facturas y recibos.
- [ ] Esquemas de salida JSON y CSV con validación.
- [ ] Historial local opcional sin retener documentos por defecto.
- [ ] Accesibilidad, traducción y pruebas de interfaz.

## v1.0 - Estabilización

- [ ] Guía de despliegue y seguridad revisada.
- [ ] APIs y modelos de datos versionados.
- [ ] Benchmarks diversos y repetibles.
- [ ] Publicación versionada con notas de lanzamiento.

> El roadmap expresa intenciones; no son funciones disponibles en v0.1.0.
