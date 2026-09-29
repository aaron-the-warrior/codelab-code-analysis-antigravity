<#
.SYNOPSIS
  Crea el repositorio Git del taller con dos ramas:
    - main                  : API de inventario "limpia"
    - refactor/analysis-demo: refactor con vulnerabilidades intencionales

.EJEMPLO
  .\scripts\preparar_repo.ps1
  .\scripts\preparar_repo.ps1 -Destino "C:\talleres\inventario-api"
#>
param(
    [string]$Destino = (Join-Path $HOME "inventario-api")
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot

if (Test-Path $Destino) {
    Write-Host "La carpeta $Destino ya existe. Bórrala o usa -Destino con otra ruta." -ForegroundColor Yellow
    exit 1
}

# 1. Copiar el código base
Copy-Item -Recurse (Join-Path $Raiz "inventario-api") $Destino
Set-Location $Destino

# 2. Rama main con el código limpio
git init -b main | Out-Null

# Asegurar identidad de Git en el repo para evitar fallos si es una instalación nueva
if (-not (git config user.name)) {
    git config user.name "Participante Taller"
}
if (-not (git config user.email)) {
    git config user.email "taller@antigravity.dev"
}

git add .
git commit -q -m "feat: API de gestión de inventario inicial"

# 3. Rama refactor/analysis-demo con los cambios a revisar
git checkout -q -b refactor/analysis-demo
Copy-Item (Join-Path $Raiz "cambios_refactor\*") $Destino -Force
git add .
git commit -q -m "refactor: nuevos endpoints de búsqueda, exportación y administración"

Write-Host ""
Write-Host "Repositorio listo en: $Destino" -ForegroundColor Green
git log --oneline --all --graph
Write-Host ""
Write-Host "Siguiente paso:  cd $Destino ; agy" -ForegroundColor Cyan
