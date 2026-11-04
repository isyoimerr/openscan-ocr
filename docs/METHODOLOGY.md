# Metodología y alcance del benchmark

## Pregunta

¿Cómo varían los errores del OCR cuando cambiamos el preprocesamiento y el modo de segmentación de página (PSM)?

## Datos

Se genera un único texto de factura ficticia, visible en `examples/factura_referencia.txt`, y tres imágenes basadas en ese mismo contenido:

- `factura_01_limpia.png`: imagen limpia.
- `factura_02_inclinada.png`: leve rotación y desenfoque.
- `factura_03_ruido.png`: sombra y ruido artificiales con semilla fija.

El PDF `examples/facturas_demo_3paginas.pdf` contiene estas tres páginas como imágenes y originalmente **no** incluye una capa de texto.

Todos los documentos son **sintéticos**. Los datos comerciales son ficticios y no deben usarse como factura real.

## Diseño experimental

1. Motor: Tesseract OCR (idioma `spa`).
2. Preprocesamiento: `original`, `otsu` o `adaptive`.
3. Modo PSM: `4`, `6` u `11`.
4. Combinaciones: 3 imágenes × 3 tratamientos × 3 PSM = **27** ejecuciones.
5. Variables registradas: CER, WER, tiempo, versión de Tesseract y hash SHA-256 de la imagen.

## Indicadores

- **CER:** distancia de edición a nivel de caracteres dividida por el número de caracteres del texto real.
- **WER:** distancia de edición a nivel de palabras dividida por el número de palabras del texto real.
- **Tiempo:** segundos de ejecución de la llamada al motor OCR, dependiente de la máquina.

Se normalizan los espacios en blanco, pero no se eliminan números, signos ni mayúsculas. Los CER/WER pueden superar 100 % cuando el sistema introduce mucho texto incorrecto. **Sin transcripción real, el CER se deja vacío**; no se reemplaza por cero.

## Reproducibilidad

```bash
python -m pip install -e .
python research/run_benchmark.py
```

El archivo `research/resultados_tesseract.csv` es una medición local incluida como ejemplo. Las duraciones pueden cambiar según CPU, versión de Tesseract, idioma y sistema operativo. No se garantiza que todas las instalaciones obtengan resultados idénticos.

## Limitaciones

Los datos son poco variados y generados sintéticamente; no permiten afirmar que un umbral, PSM o modelo de IA sea superior en documentos reales. Para establecer conclusiones generales harían falta múltiples conjuntos de documentos autorizados, muestras diversas, repeticiones, intervalos de confianza y análisis por tipo documental.

La comparación con Gemini debe registrar la versión exacta del modelo, prompts, fecha de ejecución, tokens, fallos y texto transcrito, manteniendo las claves API fuera del repositorio. No se publica una comparación Gemini vs Tesseract como resultado reproducido por este repositorio: **el CSV de la ejecución previa con Gemini no forma parte de los archivos originales recibidos**.

## Privacidad y ética

No introduzcas secretos, datos de clientes o registros personales sin permiso. Si participas en nuevos benchmarks, comparte solamente documentos sintéticos o completamente anonimizados y autorizados.
