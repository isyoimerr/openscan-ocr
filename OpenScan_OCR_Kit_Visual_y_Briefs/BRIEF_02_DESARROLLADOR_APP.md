# BRIEF — Desarrollador OpenScan OCR / calidad y estabilidad

**Repositorio:** https://github.com/isyoimerr/openscan-ocr
**Servicio Render existente:** https://openscan-ocr.onrender.com/
**Panel del servicio existente:** https://dashboard.render.com/web/srv-dblrcv59el5s73eic4ug
**Rama principal:** `main`

La aplicación ya está publicada. **No crees otro servicio en Render ni otro repositorio.** Continúa en el proyecto existente; corrige y prueba el flujo antes de darlo por estable.

## Error real reproducido
Al procesar `facturas_escaneadas_3paginas.pdf` (~1,1 MB), el usuario observó «3 páginas procesadas», «2 lecturas completadas», «790 caracteres», «60.12 s» y el error `Tesseract process timeout` en la página 3. Esto es **un procesamiento parcial**, no un éxito completo.

## Prioridades (en este orden)
1. **Reproducir el error** en la app local y, si es posible, en el servicio existente de Render usando muestras sintéticas. Medir tiempo por página, conversión de PDF, tamaño de imagen, memoria y timeout por operación. `src/openscan/engines.py` usa actualmente `pytesseract.image_to_string(... timeout=45)`; `src/openscan/export.py` hace OCR adicional al generar PDF buscable, también con timeout. No aumentes el timeout a ciegas: optimiza rasterización, tamaño, preprocesamiento y presupuesto de recursos en el hosting gratuito.
2. **Corregir el flujo parcial** sin perder las páginas que sí salieron bien. Mostrar claramente páginas intentadas, completadas y fallidas; causas, duración y opciones de reintentar página fallida. Evitar que «páginas procesadas» cuente fallos como éxitos. No reportar CER/WER si no existe referencia válida.
3. **Revisar exportaciones**: CSV, ZIP de textos y PDF buscable. Probar PDF con varias páginas, caracteres especiales y salida parcial. El PDF buscable actualmente reejecuta Tesseract; evitar trabajo duplicado cuando sea posible o explicar que es una nueva operación. No ofrecer PDF incompleto como si contuviera todas las páginas; informar exclusiones o fallos.
4. **Usabilidad pública**: en la interfaz «Tesseract (local)» debe aclararse «local en el servidor» (el navegador envía el documento a Render). Mostrar progreso real, mensajes de error comprensibles, manejo de sesiones y límites por archivo y lote.
5. **Seguridad básica**: validar el contenido real de las cargas, limitar memoria/páginas y evitar documentos persistentes o logs con contenido sensible. Mantener `OPENSCAN_ENABLE_CLOUD=false` en Render. No habilitar Gemini con clave de propietario en demo pública sin cuota, autenticación o mecanismo de protección.
6. **CI y pruebas**: incluir tests para 1 pág. válida, 3 págs. válidas, 1 fallo por timeout, exportación y validación; ejecutar la suite y confirmar el workflow `.github/workflows/ci.yml` en GitHub. Agregar un smoke test real en la app desplegada con documentos ficticios.
7. **Desplegar correcciones**: hacer commits limpios (preferiblemente PR revisable), integrar `main`, comprobar autodeploy del **servicio ya creado** y visitar la URL real. No duplicar Blueprint ni contratar plan pago. No utilizar `git push --force`.
8. **Actualizar documentación técnica**: las rutas/comandos que cambien y limitaciones conocidas. Deja el rediseño editorial del README y el logo al diseñador; coordina para evitar conflictos.

## Criterios de aceptación
- El PDF ficticio de 3 páginas termina sin timeout **o** el sistema maneja y comunica el fallo con precisión y permite recuperación; nunca presenta el lote parcial como 100 % exitoso.
- CSV y ZIP se descargan y contienen solo operaciones correctas, con informe explícito de las fallidas. PDF buscable verificado: contenido de páginas y texto seleccionable.
- Un documento de prueba pequeño funciona en la URL pública `https://openscan-ocr.onrender.com/`.
- CI verde, sin credenciales en commits ni logs, con límites documentados de Render Free.
- Se entregan capturas **reales, limpias y nuevas** de carga, OCR lado a lado, métricas y descarga para que el diseñador pueda incorporarlas al README.

**Entrega:** commits/PRs, resultados de pruebas reproducibles, evidencia del despliegue actual, incidencias pendientes y 4 screenshots limpios. Ejecuta la reparación; no te quedes en informes intermedios. Solicita autorización solo para permisos, gastos o cambios destructivos.
