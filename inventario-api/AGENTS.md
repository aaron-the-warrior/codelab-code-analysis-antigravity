# Reglas de Proyecto: Taller de Análisis de Código con Antigravity CLI

Este archivo orienta el comportamiento de **Antigravity CLI (`agy`)** mientras trabajas en este repositorio.

## 🎯 Objetivo del Proyecto
Revisar la calidad y la seguridad de los cambios de la rama `refactor/analysis-demo` de una API de inventario escrita en **FastAPI + SQLAlchemy + SQLite**.

> ⚠️ El código contiene vulnerabilidades **intencionales**. No lo despliegues ni expongas la API a Internet.

## 🌐 Idioma y Estilo de Comunicación
- **Idioma obligatorio**: todas las explicaciones, reportes, comentarios de PR y comentarios en el código deben estar en **Español**.
- Cada hallazgo debe incluir: **archivo y línea**, **severidad** (Crítica / Alta / Media / Baja), **categoría OWASP Top 10** cuando aplique, **explicación** y **corrección sugerida con código**.
- No inventes hallazgos: si no estás seguro, márcalo como "Por confirmar".

## 💻 Entorno y Herramientas
- Terminal: **Windows PowerShell** o **Bash** (Linux / macOS). Cuando sugieras comandos, da ambas versiones.
  - PowerShell: variables `$env:VARIABLE = "valor"`, continuación de línea con backtick ( ` ).
  - Bash: variables `export VARIABLE="valor"`, continuación de línea con backslash ( \ ).
- Gestor de dependencias de Python: **uv** (`uv sync`, `uv run`).
- Compara siempre contra la rama `main` (`git diff main...HEAD`).

## 🔒 Límites
- No hagas `git push`, no cierres PRs y no publiques comentarios en GitHub sin que el usuario lo pida explícitamente.
- No leas ni muestres el contenido de archivos `.env` ni de `.agents/mcp_config.json`.
