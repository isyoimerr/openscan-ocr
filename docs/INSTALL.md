# Instalación y ejecución

## Requisitos

- Python 3.10 o posterior.
- Tesseract OCR con el paquete de idioma que utilices (`spa` para español).
- Un navegador actualizado.
- No necesitas cuenta de pago ni API para el OCR local.

## Linux (Ubuntu / Debian)

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[web]'
streamlit run app/streamlit_app.py
```

## macOS

```bash
brew install tesseract tesseract-lang
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[web]'
streamlit run app/streamlit_app.py
```

## Windows

1. Instala Tesseract OCR para Windows y asegúrate de que `tesseract.exe` esté accesible desde la variable `PATH`.
2. En PowerShell, dentro de la carpeta del repositorio:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[web]"
streamlit run app/streamlit_app.py
```

Si Windows no detecta `tesseract`, reinicia la terminal después de actualizar `PATH`. Para probar `tesseract --list-langs`, debería aparecer `spa` si deseas reconocer español.

## Google Colab

Abre `research/openscan_public_demo.ipynb` con [Google Colab](https://colab.research.google.com/). El cuaderno instala las dependencias y obtiene las muestras desde el repositorio público. Para usar imágenes propias, cambia la ruta de ejemplo en la celda indicada.

## Gemini opcional

OpenScan no necesita Gemini para leer documentos. Si deseas habilitarlo:

1. Obtén una clave válida para Gemini API.
2. **No la escribas en el código.** Establécela en el ambiente como `GEMINI_API_KEY` o en `.streamlit/secrets.toml` (archivo ignorado por Git):

```toml
GEMINI_API_KEY = "tu_clave_privada"
GEMINI_MODEL = "modelo_valido_para_tu_cuenta"
```

3. Establece `OPENSCAN_ENABLE_CLOUD=true` solo en un entorno privado o controlado. En una aplicación pública, cualquier visitante podría consumir la cuota de tu clave del servidor.
4. Reinicia Streamlit. Gemini aparecerá como un motor opcional. Puede haber cuotas, cobros, restricciones de acceso y errores transitorios `429/503`. El valor `GEMINI_MODEL` se puede cambiar según los modelos disponibles en tu cuenta.

En Google Colab, el cuaderno lee el secreto `API` mediante `google.colab.userdata.get('API')`; no muestra ni publica su valor.

## Desplegar en Streamlit Community Cloud

Publica este repositorio y selecciona:

- Repositorio: `isyoimerr/openscan-ocr`.
- Rama: `main`.
- Archivo de entrada: `app/streamlit_app.py`.

El archivo `requirements.txt` instala las dependencias Python y `packages.txt` declara Tesseract y el idioma español. Comprueba los límites y la disponibilidad del servicio antes de usarlo públicamente. Configura secretos desde los ajustes de la plataforma, **no** mediante commits.

## Solución de problemas

- `TesseractNotFoundError`: instala el ejecutable Tesseract y comprueba el `PATH`.
- `Error opening data file spa`: instala el idioma `spa` o elige uno presente en `tesseract --list-langs`.
- `Gemini 503`: servicio temporalmente saturado; prueba más tarde o utiliza Tesseract local.
- `CER = N/D`: se debe a que no se aportó un texto real de referencia; no es un fallo.
