# OpenScan OCR — Kit de capturas para README y producto

**Proyecto:** https://github.com/isyoimerr/openscan-ocr  
**Demo:** https://openscan-ocr.onrender.com/  
**Fecha:** 4 de noviembre de 2026

## Cómo usar este kit

Este kit contiene **cinco capturas originales únicas** tomadas de la aplicación y del README en GitHub, sin retocar ni alterar. La sexta captura recibida era un duplicado exacto de la quinta y se omitió deliberadamente.

### 1. Captura candidata para publicar

| Archivo | Resolución | Uso sugerido |
|---|---|---|
| `capturas_para_readme/01_interfaz_carga_documentos.png` | 958 × 523 | Mostrar el formulario de carga como captura provisional. Reemplazar por una captura nueva a resolución más alta tras el pulido visual. |

### 2. Referencias internas; NO publicarlas todavía en el README

| Archivo | Resolución | Por qué no es material promocional final |
|---|---|---|
| `referencias_para_mejorar/02_comparacion_imagen_texto_leyenda_academica.png` | 983 × 587 | Muestra lectura OCR real, pero el documento ficticio incluye referencia académica. Repetir con una muestra neutra. |
| `referencias_para_mejorar/03_descargas_con_error_timeout.png` | 959 × 492 | Presenta la sección de descargas junto con un error de procesamiento. Se debe repetir sin el aviso. |
| `referencias_para_mejorar/04_estado_procesamiento_parcial_2_de_3.png` | 1365 × 606 | Evidencia: 3 páginas intentadas, 2 lecturas terminadas y `Tesseract process timeout` en la tercera. Usar para depurar la UX. |
| `referencias_para_mejorar/05_readme_actual_badges_rotos.png` | 781 × 602 | Estado anterior del README; algunos badges o imágenes fallan. Usar solo para rediseño/QA. |

## Capturas definitivas por producir (después de corregir el timeout)

1. `assets/screenshots/01-carga-documentos.png` — vista inicial limpia, sin documentos personales.
2. `assets/screenshots/02-documento-y-texto.png` — visualización lado a lado con factura totalmente ficticia y transcripción sin errores visibles.
3. `assets/screenshots/03-metricas.png` — tiempo y resumen con 100 % de operaciones completadas en un caso comprobado; sin inventar CER.
4. `assets/screenshots/04-exportaciones.png` — descargas TXT/ZIP/CSV y PDF buscable verificadas en la app.

**Preferencias:** ancho real >= 1400 px cuando sea posible; recorte consistente; sin bordes de navegador, datos privados, marcas de agua, diálogos de error ni fechas ficticias presentadas como datos reales. Usar texto alternativo descriptivo. No simular capturas exitosas con herramientas gráficas; recapturar desde la app funcionando. Si se usa un gráfico de benchmark, citar `research/resultados_tesseract.csv` y explicar que son documentos sintéticos.

## Ubicación final en GitHub

Copiar únicamente las capturas aprobadas a `assets/screenshots/` dentro del repositorio. No subir todo el kit al README. Las capturas de fallos pueden adjuntarse a un issue de GitHub para trazabilidad.

## Recomendación editorial

En el README, priorizar la secuencia **problema → enfoque técnico → arquitectura → análisis reproducible → evolución de versiones → demo real → cómo ejecutar → cómo contribuir**. El README debe estar enfocado en ingeniería y resultados, no en promoción ni en historia académica.

**Enlace principal que debe aparecer muy visible:** https://openscan-ocr.onrender.com/ (sin parámetros de seguimiento).
