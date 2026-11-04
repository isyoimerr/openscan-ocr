# Publicar OpenScan OCR en GitHub

## 1. Crear un repositorio vacío

Entra en https://github.com/new y utiliza:

- **Owner:** `isyoimerr`
- **Repository name:** `openscan-ocr`
- **Description:** `Open-source OCR for scanned documents: local Tesseract, optional Gemini, reproducible benchmarks and a web interface.`
- **Visibility:** Public

**No marques** las opciones para crear README, `.gitignore` o licencia: el paquete ya los contiene.

## 2. Subir el proyecto

Descomprime el ZIP recibido y abre una terminal **dentro de la carpeta `openscan-ocr`**:

```bash
git init
git branch -M main
git add .
git commit -m "feat: publish OpenScan OCR v0.1.0"
git remote add origin https://github.com/isyoimerr/openscan-ocr.git
git push -u origin main
```

Necesitas iniciar sesión en GitHub en tu equipo. Si prefieres la interfaz web, crea el repositorio vacío y usa **Add file > Upload files** para cargar los archivos y carpetas descomprimidos; **no subas el ZIP sin extraer**.

## 3. Verificar

- El README aparece automáticamente en la portada.
- En **Actions**, la ejecución `Tests` finaliza correctamente.
- Entra al cuaderno con el enlace **Ver el cuaderno en Colab** del README.
- Para abrir la interfaz al publico, sigue [Despliegue en Render](DEPLOY_RENDER.md) usando `render.yaml`.

## 4. Primera publicación versionada (opcional)

En GitHub, selecciona **Releases > Draft a new release**, crea la etiqueta `v0.1.0` y describe las funciones de esta versión. No publiques claves API, archivos de uso personal ni documentos reales.
