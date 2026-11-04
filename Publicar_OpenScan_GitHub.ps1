# OpenScan OCR - publicacion inicial en un repositorio GitHub vacio.
# Requisitos: Git instalado, acceso a GitHub desde Git Credential Manager.
# Coloca este archivo al lado de OpenScan_OCR_Render_Listo.zip y ejecuta:
#   powershell -ExecutionPolicy Bypass -File .\Publicar_OpenScan_GitHub.ps1

$ErrorActionPreference = 'Stop'
$repo = 'https://github.com/isyoimerr/openscan-ocr.git'
$zip = Join-Path $PSScriptRoot 'OpenScan_OCR_Render_Listo.zip'
$temp = Join-Path $env:TEMP ('openscan-publicar-' + [guid]::NewGuid().ToString('N'))

function Run-Git {
    & git @args
    if ($LASTEXITCODE -ne 0) { throw "Git fallo (codigo $LASTEXITCODE): $($args -join ' ')" }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Instala Git for Windows antes de ejecutar este script.'
}
if (-not (Test-Path -LiteralPath $zip)) {
    throw "No se encontro el ZIP junto a este script: $zip"
}

Write-Host 'Comprobando que el repositorio remoto este vacio...'
$heads = & git ls-remote --heads $repo
if ($LASTEXITCODE -ne 0) { throw 'No se pudo comprobar el repositorio en GitHub.' }
if ($heads) {
    throw 'El repositorio ya tiene commits. No se publica para evitar sobrescribir trabajo existente.'
}

try {
    New-Item -ItemType Directory -Force -Path $temp | Out-Null
    Expand-Archive -LiteralPath $zip -DestinationPath $temp -Force
    $source = Join-Path $temp 'openscan-ocr'
    if (-not (Test-Path (Join-Path $source 'Dockerfile'))) {
        throw 'El ZIP no contiene la estructura esperada de OpenScan OCR.'
    }
    Set-Location $source
    Run-Git init
    Run-Git add --all
    Run-Git commit -m 'feat: publish OpenScan OCR v0.1.0'
    Run-Git branch -M main
    Run-Git remote add origin $repo

    Write-Host "Se publicara el proyecto en $repo"
    $answer = Read-Host 'Para confirmar, escribe PUBLICAR'
    if ($answer -cne 'PUBLICAR') { throw 'Publicacion cancelada.' }

    Run-Git push -u origin main
    Write-Host 'Publicacion completada. Repositorio: https://github.com/isyoimerr/openscan-ocr'
}
finally {
    Set-Location $PSScriptRoot
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
}
