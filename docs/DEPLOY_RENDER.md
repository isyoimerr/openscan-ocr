# Desplegar OpenScan OCR en Render

Guía para publicar una **demo** abierta al público. No es una configuración endurecida para producción.

## Antes de empezar

- El repositorio `isyoimerr/openscan-ocr` debe existir en GitHub y contener el proyecto.
- Usa la rama `main` y comprueba que GitHub Actions / Tests pase.
- No subas `.env`, `secrets.toml`, claves ni documentos privados.
- El `Dockerfile` instala Tesseract y el idioma español. No hace falta Colab en el servidor.

## Despliegue con Blueprint

1. En [Render Dashboard](https://dashboard.render.com/), selecciona **New > Blueprint**.
2. Conecta tu cuenta de GitHub y el repositorio `isyoimerr/openscan-ocr`.
3. Render detectará `render.yaml`. Revisa el servicio `openscan-ocr`, plan `free` y su región.
4. Confirma la creación del servicio. Si Render solicita una acción de facturación, revísala antes de autorizarla.
5. Verifica que el deploy termine en **Live** y abre la URL HTTPS que Render asigne.
6. Comprueba `/_stcore/health` (debería devolver OK), sube `examples/recibo_demo.png` y descarga TXT/CSV.

Render ejecuta el contenedor del `Dockerfile`, que escucha en `0.0.0.0` y `${PORT:-10000}`. No hace falta agregar un despliegue extra desde GitHub Actions: `autoDeployTrigger: checksPass` espera que los checks pasen antes del auto-deploy.

## Configuración y límites de esta demo

- Motor público: **Tesseract**. No necesita clave ni pago por solicitud OCR.
- Gemini desactivado (`OPENSCAN_ENABLE_CLOUD=false`). No configurar claves privadas en el repositorio.
- Hasta 4 archivos por lote, 10 MB por archivo, 20 MB combinados, 5 páginas totales y 12 megapíxeles por página.
- Los resultados están en memoria de la sesión, sin base de datos ni almacenamiento permanente configurado.
- No utilices esta instancia pública con recibos reales, historia clínica, identificación, información bancaria o documentos confidenciales.
- No existe autenticación ni control de cuotas por IP; no debe considerarse producción. Si se vuelve popular, añade rate limiting, cuotas y autenticación antes de abrir procesamiento ilimitado.
- En Render Free hay memoria/CPU limitadas, posible suspensión por inactividad y reinicios. Revisa [limitaciones de Render Free](https://render.com/docs/free). No garantizamos tiempos de respuesta.

## Activar Gemini solo con control de acceso

En Render > Environment define `GEMINI_API_KEY` como secreto y `OPENSCAN_ENABLE_CLOUD=true` **solo si restringes el acceso** o aceptas que cualquiera podrá gastar la cuota del proyecto. La clave nunca debe aparecer en el repositorio. `GEMINI_MODEL` es opcional y debe ser un modelo disponible para esa clave.

## Diagnóstico

- **Build failed**: revisa logs de instalación de Python/Tesseract y dependencias.
- **No open ports detected**: el `Dockerfile` debe usar `PORT` y `--server.address=0.0.0.0`.
- **Health check failed**: revisa `/_stcore/health` y logs al arrancar Streamlit.
- **OOM / restart**: disminuye el número de páginas, tamaño de imágenes o usa un plan con más memoria.
- **Gemini 403/429/503**: mantenlo apagado en el despliegue público; usa Tesseract.

## Prueba en Docker local

```bash
docker build -t openscan-ocr .
docker run --rm -p 10000:10000 -e PORT=10000 -e OPENSCAN_ENABLE_CLOUD=false openscan-ocr
```

Abre `http://localhost:10000`, carga una imagen ficticia y verifica descargas.
