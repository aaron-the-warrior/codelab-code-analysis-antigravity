#!/usr/bin/env bash
# Crea el repositorio Git del taller con dos ramas:
#   - main                  : API de inventario "limpia"
#   - refactor/analysis-demo: refactor con vulnerabilidades intencionales
#
# Uso:
#   bash scripts/preparar_repo.sh
#   bash scripts/preparar_repo.sh ~/talleres/inventario-api
set -euo pipefail

DESTINO="${1:-$HOME/inventario-api}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

if [ -e "$DESTINO" ]; then
  echo "La carpeta $DESTINO ya existe. Bórrala o indica otra ruta como argumento."
  exit 1
fi

# 1. Copiar el código base
cp -r "$RAIZ/inventario-api" "$DESTINO"
cd "$DESTINO"

# 2. Rama main con el código limpio
git init -q -b main

# Asegurar identidad de Git en el repo para evitar fallos si es una instalación nueva
if ! git config user.name >/dev/null 2>&1; then
  git config user.name "Participante Taller"
fi
if ! git config user.email >/dev/null 2>&1; then
  git config user.email "taller@antigravity.dev"
fi

git add .
git commit -q -m "feat: API de gestión de inventario inicial"

# 3. Rama refactor/analysis-demo con los cambios a revisar
git checkout -q -b refactor/analysis-demo
cp "$RAIZ"/cambios_refactor/* "$DESTINO"/
git add .
git commit -q -m "refactor: nuevos endpoints de búsqueda, exportación y administración"

echo
echo "Repositorio listo en: $DESTINO"
git log --oneline --all --graph
echo
echo "Siguiente paso:  cd $DESTINO && agy"
