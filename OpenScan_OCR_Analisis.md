# Resultados exploratorios | OpenScan OCR

## Resumen

Se realizaron **27 lecturas locales** con Tesseract 5.5.0, usando 3 versiones de una factura ficticia, 3 tratamientos de imagen y 3 modos PSM. El experimento no consume una API externa.

El indicador principal es CER (tasa de error por caracteres) frente a un texto de referencia. **Cuanto menor es, mejor.** El tiempo corresponde a esta ejecución local y depende del equipo.

## 1. Efecto del preprocesamiento

| Tratamiento | CER medio | WER medio | Tiempo medio |
| --- | ---: | ---: | ---: |
| Sin binarizar | 1.67 % | 5.42 % | 0.514 s |
| Otsu | 1.15 % | 4.07 % | 0.277 s |
| Adaptativa | 1.15 % | 3.52 % | 0.272 s |

![CER medio por preprocesamiento](figures/cer_preprocesamiento.png)

En este conjunto pequeño, Otsu y adaptativa empataron en CER medio. Que un tratamiento mejore algunas imágenes **no implica** que funcione mejor con todos los documentos.

## 2. Modo de segmentación (PSM)

| PSM | CER medio | WER medio | Tiempo medio |
| --- | ---: | ---: | ---: |
| 4 | 0.11 % | 0.81 % | 0.353 s |
| 6 | 0.04 % | 0.27 % | 0.345 s |
| 11 | 3.81 % | 11.92 % | 0.366 s |

![CER medio por PSM](figures/cer_psm.png)

PSM 6 obtuvo el CER medio más bajo en esta muestra; PSM 11 introdujo más diferencias. La estructura de las facturas influye en el resultado. En nuevos documentos debe repetirse el análisis antes de elegir un modo definitivo.

## 3. Limitaciones y siguiente experimento

- Solo se evaluaron tres imágenes sintéticas derivadas de un mismo contenido: la muestra es pequeña y poco diversa.
- CER y WER utilizan referencia conocida. En documentos del usuario sin referencia se dejan vacíos.
- Los tiempos no son comparables entre máquinas diferentes sin controlar hardware y software.
- **Gemini** es una integración opcional. No se reporta una superioridad numérica sin un registro exportado y reproducible del experimento.
- Próximo paso: más documentos sintéticos de varios tipos y revisión humana de campos extraídos.

## Reproducir

```bash
python research/run_benchmark.py
```

El conjunto y los resultados fila a fila están disponibles en [`examples/`](../examples/) y [`resultados_tesseract.csv`](resultados_tesseract.csv). Consulta la [metodología](../docs/METHODOLOGY.md) para entender el cálculo exacto.
