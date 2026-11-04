# Contribuir a OpenScan OCR

Gracias por ayudar a construir herramientas de reconocimiento de texto más accesibles.

## Antes de empezar

1. Revisa los issues abiertos y describe la mejora que propones.
2. Trabaja en una rama con un nombre claro: `feat/...`, `fix/...` o `docs/...`.
3. Agrega pruebas para cambios de código; actualiza la documentación cuando cambie una función.
4. Abre un pull request explicando qué problema resuelve y cómo se comprobó.

## Preparar entorno de contribución

```bash
python -m pip install -e '.[dev,web]'
pytest -q
python research/run_benchmark.py
```

## Datos de prueba

Comparte solo documentos sintéticos, de dominio público o autorizados y correctamente anonimizados. No compartas claves API, datos de clientes, números de identificación reales ni facturas privadas.

## Estándares mínimos

- Documenta el tratamiento y cualquier supuesto de calidad.
- No presentes CER/WER si no existe transcripción real.
- Separa los motores OCR del código de interfaz para facilitar las pruebas.
- Mantén Tesseract local como opción gratuita y funcional.
