# BRIEF — Editor de README y diseñador de identidad

**Proyecto:** OpenScan OCR
**Repositorio:** https://github.com/isyoimerr/openscan-ocr
**Demo real:** https://openscan-ocr.onrender.com/
**Licencia:** MIT
**Estado:** prototipo público / beta en validación; no presentarlo como producción estable.

Eres responsable de **identidad visual, estrategia editorial, assets y README**, no de arreglar el motor OCR. Tienes acceso al proyecto completo y al kit de capturas. Revisa los archivos reales antes de escribir; evita afirmaciones no verificadas.

## Dirección editorial
Presentar OpenScan como proyecto tecnológico open source, construido de forma incremental, con investigación reproducible y una utilidad práctica para convertir fotografías y PDF escaneados en texto, CSV y PDF buscable. No menciones universidad, profesor, tarea ni expresiones académicas. Evita promesas de precisión universal y publicidad exagerada.

El lector debe entender en este orden:
1. **Identidad y valor:** nombre, frase breve, enlace claro a la demo y al código.
2. **Problema y propuesta:** PDF escaneado / fotografía → texto utilizable.
3. **Cómo está construido:** pipeline de entrada, render PDF, preprocesamiento, motor Tesseract, métricas y exportación; Gemini como módulo opcional no habilitado en la demo pública.
4. **Investigación y evidencia:** 27 experimentos sintéticos, CER y WER con referencia; metodología y límites, sin fingir resultados externos.
5. **Evolución real:** de notebook/benchmark a motor Python reutilizable y a interfaz web; roadmap de mejoras aún no implementadas.
6. **Producto y demostración:** enlace a `https://openscan-ocr.onrender.com/` y capturas definitivas reales de la app.
7. **Cómo reproducirlo:** instalación, comandos probados, Colab público y acceso a archivos de muestra.
8. **Open source y contribuciones:** qué contribuciones buscamos, licencia MIT, issues y PR; equipo/contacto solo si están autorizados.

## Diseño
- Construye un logotipo original, simple y técnico (icono vectorial SVG y variante para fondo claro/oscuro). Entrega también una versión PNG para previsualizaciones, sin insertar fuentes de terceros no licenciadas.
- Crea estilo consistente: tipografía legible, paleta sobria alineada con la app (oscuro, blanco y acento turquesa). Nada de saturar con badges o banners.
- Diseña un README nativo de GitHub: máximo 1 hero modesto, enlaces claros, tabla de capacidades real y 2–4 capturas útiles. No incrustes imágenes enormes antes del problema y de la explicación técnica.
- Prepara `assets/brand/` y `assets/screenshots/` con nombres cortos y estables. Comprueba que rutas relativas y enlaces externos resuelvan bien en GitHub.
- En la parte superior: `[Probar demo](https://openscan-ocr.onrender.com/)`, `[Ver análisis](research/ANALISIS_RESULTADOS.md)`, `[Abrir Colab](https://colab.research.google.com/github/isyoimerr/openscan-ocr/blob/main/research/openscan_public_demo.ipynb)` y `[Contribuir](CONTRIBUTING.md)`.
- El README actual muestra badges de Python/licencia/estado rotos en la captura. Elimínalos o reemplázalos por una presentación que hayas verificado. El estado de CI se puede mostrar si realmente está pasando.

## Capturas y restricciones
- El kit incluye 5 capturas originales; solo `capturas_para_readme/01_interfaz_carga_documentos.png` es una candidata provisional.
- Las otras cuatro están en `referencias_para_mejorar/` porque muestran timeout, badges rotos o una referencia académica en el documento ficticio. **No las publiques como screenshots finales.**
- Coordina con el desarrollador para repetir capturas tras corregir el timeout. Usa un documento ficticio neutral, sin datos personales ni leyendas académicas.
- No inventes ni retoques resultados OCR para producir una imagen de éxito. Publica capturas de una ejecución real verificada.

## Validaciones antes de entregar
- README probado en GitHub web y móvil, imágenes visibles y links correctos.
- No afirmar que Gemini está activo en la web: allí está deshabilitado.
- Separar «disponible», «beta» y «planificado» en las funcionalidades.
- Mencionar que Tesseract corre en el **servidor de la demo**, no en la máquina del visitante, y advertir que no se suba información sensible.
- Documentar límites del conjunto de pruebas sintéticas; nada de «99 % garantizado».

**Entrega:** propuesta de marca + logo SVG/PNG + README reescrito y renderizado + carpeta assets ordenada + enlaces probados + breve registro de cambios. Implementa los cambios en tu rama y coordina la integración con el desarrollador. No te detengas en auditorías repetidas: ejecuta y valida.
