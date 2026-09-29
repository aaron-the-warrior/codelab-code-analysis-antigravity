# 🔎 Revisión de Código y Análisis de Seguridad con Antigravity CLI

> **⚡ Powered by aaronthewarrior**
> Repositorio base, adaptación práctica y curaduría técnica creada por [aaronthewarrior](https://github.com/aaron-the-warrior).

[![Powered by](https://img.shields.io/badge/Powered%20by-aaronthewarrior-blueviolet?style=for-the-badge&logo=github)](https://github.com/aaron-the-warrior)
[![Antigravity CLI](https://img.shields.io/badge/Google-Antigravity%20CLI%20(agy)-4285F4?style=for-the-badge&logo=google)](https://antigravity.google/docs/cli/install/)
[![LLM](https://img.shields.io/badge/Model-Gemini%203.8%20Flash-orange?style=for-the-badge&logo=googlegemini)](https://aistudio.google.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.12-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OWASP](https://img.shields.io/badge/OWASP-Top%2010-000000?style=for-the-badge&logo=owasp&logoColor=white)](https://owasp.org/Top10/)
[![PowerShell](https://img.shields.io/badge/Windows-PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white)](#-prerrequisitos-y-configuración-del-entorno)
[![Linux](https://img.shields.io/badge/Linux-Bash-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#-prerrequisitos-y-configuración-del-entorno)

Guía práctica paso a paso para usar **Antigravity CLI (`agy`)** como revisor de código y analista de seguridad. Vas a trabajar sobre una API de inventario en **FastAPI** a la que un "refactor" le metió vulnerabilidades del **OWASP Top 10**, y vas a:

- Instalar los plugins oficiales de **revisión de código** y **seguridad**.
- Ejecutar análisis **interactivos** y **automáticos (headless)**.
- Conectar el **servidor MCP de GitHub** para publicar el reporte como comentario en un Pull Request.
- Llevar todo a **CI/CD con GitHub Actions**.
- *(Bonus)* Pedirle a `agy` que **corrija** las vulnerabilidades y comprobarlo.

> [!TIP]
> El taller se realiza en **Windows PowerShell**. Cada comando incluye también su equivalente para **Linux / macOS (Bash)**. Si no puedes instalar nada en tu equipo, usa el [Plan B: Google Cloud Shell](#-plan-b-google-cloud-shell).

> [!CAUTION]
> La API de este taller es **vulnerable a propósito**. Nunca la despliegues ni la expongas a Internet.

---

## 📑 Temario

 1. [Créditos y Cita de la Fuente Original](#️-créditos-y-cita-de-la-fuente-original)
 2. [Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
 3. [Prerrequisitos y Configuración del Entorno](#-prerrequisitos-y-configuración-del-entorno)
 4. [Paso 1: Instalar y autenticar Antigravity CLI](#-paso-1-instalar-y-autenticar-antigravity-cli)
 5. [Paso 2: Preparar el repositorio de práctica](#-paso-2-preparar-el-repositorio-de-práctica)
 6. [Paso 3: Primeros comandos con `agy`](#-paso-3-primeros-comandos-con-agy)
 7. [Paso 4: Instalar los plugins de revisión y seguridad](#-paso-4-instalar-los-plugins-de-revisión-y-seguridad)
 8. [Paso 5: Análisis de seguridad interactivo](#️-paso-5-análisis-de-seguridad-interactivo)
 9. [Paso 6: Revisión de código en modo headless](#-paso-6-revisión-de-código-en-modo-headless)
10. [Paso 7: Servidor MCP de GitHub y comentario en el Pull Request](#-paso-7-servidor-mcp-de-github-y-comentario-en-el-pull-request)
11. [Paso 8: Automatizar en CI/CD con GitHub Actions](#️-paso-8-automatizar-en-cicd-con-github-actions)
12. [Paso 9 (Bonus): Remediación asistida](#-paso-9-bonus-remediación-asistida)
13. [Plan B: Google Cloud Shell](#-plan-b-google-cloud-shell)
14. [Limpieza de Recursos](#-limpieza-de-recursos)
15. [Solución de Problemas](#-solución-de-problemas)
16. [Recursos para Seguir Aprendiendo](#-recursos-para-seguir-aprendiendo)

---

## 🎖️ Créditos y Cita de la Fuente Original

Este repositorio y material didáctico es un proyecto **Powered by [aaronthewarrior](https://github.com/aaron-the-warrior)**, creado para traducir, actualizar y llevar al plano práctico los conceptos presentados en las fuentes oficiales de Google:

* **Autor y Curador de esta adaptación:**
  * **Aarón Guerrero**

    **Enlaces:**
    - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" width="16" height="16" align="center" /> [Google Developer Expert](https://me.developers.google.com/u/108177037637693690075)
    - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="16" height="16" align="center" /> [aaron-the-warrior](https://github.com/aaron-the-warrior)
    - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="16" height="16" align="center" /> [aaronthewarrior](https://www.linkedin.com/in/aaronthewarrior/)
    - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitter/twitter-original.svg" width="16" height="16" align="center" /> [@aaronthewarrior](https://twitter.com/aaronthewarrior)
    - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg" width="16" height="16" align="center" /> [aaron.guerrero.hernandez](https://www.facebook.com/aaron.guerrero.hernandez)

* **Codelab Oficial:**
  * *Título:* **Revisión de código y análisis de seguridad con Gemini CLI y extensiones** (*Code Review and Security Analysis with Gemini CLI with Extensions*)
  * *Plataforma:* Google Codelabs
  * *Enlace:* [https://codelabs.developers.google.com/gemini-cli-code-analysis?hl=es-419](https://codelabs.developers.google.com/gemini-cli-code-analysis?hl=es-419)

* **Repositorio de código original (API vulnerable):**
  * *Título:* **gemini-cli-code-analysis-demo**
  * *Autor:* [@alphinside](https://github.com/alphinside) — Licencia Apache 2.0
  * *Enlace:* [https://github.com/alphinside/gemini-cli-code-analysis-demo](https://github.com/alphinside/gemini-cli-code-analysis-demo)

* **Extensiones oficiales (ahora plugins de Antigravity CLI):**
  * *Security:* [https://github.com/gemini-cli-extensions/security](https://github.com/gemini-cli-extensions/security)
  * *Code Review:* [https://github.com/gemini-cli-extensions/code-review](https://github.com/gemini-cli-extensions/code-review)

* **Documentación Oficial de Antigravity CLI:**
  * *Instalación y autenticación:* [antigravity.google/docs/cli/install](https://antigravity.google/docs/cli/install/)
  * *Migración desde Gemini CLI:* [antigravity.google/docs/cli/gcli-migration](https://antigravity.google/docs/cli/gcli-migration/)
  * *Skills, MCP y modo headless:* [skills](https://antigravity.google/docs/skills/) · [mcp](https://antigravity.google/docs/mcp/) · [headless](https://antigravity.google/docs/cli/headless/)

> [!NOTE]
> Los comentarios, mensajes y docstrings del código original se tradujeron al español. La lógica de la API y las vulnerabilidades se mantienen **idénticas** al repositorio original; solo se agregó una dependencia desactualizada (`requests==2.19.1`) para practicar el escaneo de dependencias.

---

## 🏛️ Arquitectura del Proyecto

```text
codelab-code-analysis-antigravity/
├── README.md                       # Esta guía
├── inventario-api/                 # Código base de la API (rama main)
│   ├── AGENTS.md                   # Reglas para agy: todo en español, formato de hallazgos
│   ├── main.py                     # Endpoints de productos, inventario y transacciones
│   ├── models.py                   # Modelos SQLAlchemy
│   ├── schemas.py                  # Esquemas Pydantic
│   ├── database.py                 # Conexión a SQLite
│   ├── pyproject.toml              # Dependencias (uv)
│   └── README.md / LICENSE
├── cambios_refactor/               # El "refactor" con vulnerabilidades (rama refactor/analysis-demo)
│   ├── main.py
│   └── pyproject.toml
├── scripts/
│   ├── preparar_repo.ps1           # Crea el repo Git con sus dos ramas (Windows)
│   └── preparar_repo.sh            # Lo mismo para Linux / macOS
├── plantillas/
│   ├── settings.json               # Configuración de agy para usar API Key
│   ├── mcp_config.json             # Servidor MCP de GitHub
│   └── revision-agy.yml            # Workflow de GitHub Actions con agy
└── guia_instructor/
    └── hallazgos_esperados.md      # "Hoja de respuestas" con las vulnerabilidades plantadas
```

**Flujo del taller:**

```text
 main ──●── (API limpia)
         \
          ●── refactor/analysis-demo  (endpoints nuevos + vulnerabilidades)
                 │
                 ├── agy + skill security     →  security-analysis.md
                 ├── agy + skill code-review  →  code-review.md
                 └── agy + MCP de GitHub      →  comentario en el Pull Request
```

---

## ⚙️ Prerrequisitos y Configuración del Entorno

### 1. Requisitos del Sistema
* **Git** para clonar y crear ramas.
* **Python 3.12+** y **uv** (solo si quieres ejecutar la API; el análisis no lo necesita).
* **Cuenta de Google** (inicio de sesión en `agy`) **o** una **API Key de Gemini** de [Google AI Studio](https://aistudio.google.com/apikey).
* **Cuenta de GitHub** y **GitHub CLI (`gh`)** para los pasos 7 y 8.

#### En Windows (PowerShell):
```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install astral-sh.uv
winget install GitHub.cli
# Cierra y vuelve a abrir PowerShell para actualizar variables de entorno
git --version; python --version; uv --version; gh --version

# Configura tu identidad de Git (si es una instalación nueva):
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

#### En Linux o macOS:
```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y git python3 gh
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS
brew install git python gh uv

git --version && python3 --version && uv --version && gh --version

# Configura tu identidad de Git (si es una instalación nueva):
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

### 2. Clonar el material del taller

#### En Windows (PowerShell):
```powershell
cd $HOME
git clone https://github.com/aaron-the-warrior/codelab-code-analysis-antigravity.git
cd codelab-code-analysis-antigravity
```

#### En Linux o macOS:
```bash
cd ~
git clone https://github.com/aaron-the-warrior/codelab-code-analysis-antigravity.git
cd codelab-code-analysis-antigravity
```

---

## 🚀 Paso 1: Instalar y autenticar Antigravity CLI

### 1. Instalación

#### En Windows (PowerShell):
```powershell
irm https://antigravity.google/cli/install.ps1 | iex
# Cierra y vuelve a abrir PowerShell
agy --version
```

#### En Linux o macOS:
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
# Abre una terminal nueva (o ejecuta: source ~/.bashrc)
agy --version
```

### 2. Autenticación

**Opción A — Cuenta de Google (recomendada):** ejecuta `agy`. Se abrirá el navegador para iniciar sesión (en SSH te muestra una URL y un código de confirmación).

**Opción B — API Key de Gemini:** copia la plantilla de configuración y define la variable de entorno.

#### En Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\antigravity-cli" | Out-Null
Copy-Item .\plantillas\settings.json "$HOME\.gemini\antigravity-cli\settings.json"
$env:GEMINI_API_KEY = "tu-api-key-aqui"
```

#### En Linux o macOS:
```bash
mkdir -p ~/.gemini/antigravity-cli
cp plantillas/settings.json ~/.gemini/antigravity-cli/settings.json
export GEMINI_API_KEY="tu-api-key-aqui"
```

Contenido de `plantillas/settings.json`:
```json
{
  "modelProvider": "gemini",
  "model": "Gemini 3.8 Flash (Medium)",
  "toolPermission": "request-review"
}
```

> [!CAUTION]
> Si ya tienes un `settings.json` de `agy`, **no lo sobrescribas**: agrega solo la línea `"modelProvider": "gemini"`. Y nunca subas tu API Key a GitHub.

> [!TIP]
> **Compatibilidad de modelos:** si `Gemini 3.8 Flash` no está disponible en tu cuenta o región, ejecuta `agy models` para ver la lista y cambia el valor de `"model"` (por ejemplo `Gemini 3.7 Flash (Low)`).

---

## 📦 Paso 2: Preparar el repositorio de práctica

El script crea un repositorio Git nuevo en `inventario-api` (en tu carpeta de usuario) con dos ramas: `main` (código limpio) y `refactor/analysis-demo` (el refactor a revisar), igual que el repositorio del codelab original.

#### En Windows (PowerShell):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\preparar_repo.ps1
cd $HOME\inventario-api
```

#### En Linux o macOS:
```bash
bash scripts/preparar_repo.sh
cd ~/inventario-api
```

Verifica que estás en la rama del refactor y mira qué cambió (igual en PowerShell y Bash):
```bash
git branch
git diff --stat main...HEAD
```

Resultado esperado:
```text
  main
* refactor/analysis-demo
 main.py        | 176 ++++++++++++++++++++++++++++++++++++++++++++------
 pyproject.toml |   3 +-
```

### (Opcional) Ejecutar la API
```bash
uv sync
uv run fastapi dev main.py
```
Abre `http://localhost:8000/docs` para ver los endpoints. Detén el servidor con `Ctrl + C`.

---

## 💬 Paso 3: Primeros comandos con `agy`

Desde la carpeta `inventario-api`, inicia Antigravity CLI:
```bash
agy
```

> [!TIP]
> El archivo `AGENTS.md` en la raíz del repositorio le indica a `agy` que responda en español, que dé comandos para PowerShell y Bash, y el formato que deben tener los hallazgos. Si te pregunta si confías en la carpeta (*trusted workspace*), acepta.

Prueba estos comandos dentro de `agy`:

| Comando | Qué hace |
|---|---|
| `/help` | Ayuda general, comandos y atajos |
| `/skills` | Lista las skills disponibles (aquí aparecerán los plugins) |
| `/mcp` | Administrador de servidores MCP |
| `/config` | Cambia ajustes, por ejemplo el modo de permisos |
| `/plan` | Pide un plan antes de ejecutar |
| `!` | Alterna al modo shell |
| `/quit` | Sale de `agy` (también `Ctrl + D` dos veces) |

Primer prompt de calentamiento:
```text
Investiga el OWASP Top 10 más reciente y escríbelo en owasp.md: para cada categoría da una explicación breve en español y un ejemplo en Python/FastAPI.
```

---

## 🧩 Paso 4: Instalar los plugins de revisión y seguridad

Las extensiones de Gemini CLI ahora se usan como **plugins** de Antigravity CLI. Sal de `agy` (`/quit`) y sigue **una** de estas opciones.

### Opción A — Instalar desde el repositorio oficial (recomendada)

#### En Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\agy-plugins" | Out-Null
git clone --depth 1 https://github.com/gemini-cli-extensions/security "$HOME\agy-plugins\security"
git clone --depth 1 https://github.com/gemini-cli-extensions/code-review "$HOME\agy-plugins\code-review"

agy plugin install "$HOME\agy-plugins\security"
agy plugin install "$HOME\agy-plugins\code-review"
agy plugin list
```

#### En Linux o macOS:
```bash
mkdir -p ~/agy-plugins
git clone --depth 1 https://github.com/gemini-cli-extensions/security ~/agy-plugins/security
git clone --depth 1 https://github.com/gemini-cli-extensions/code-review ~/agy-plugins/code-review

agy plugin install ~/agy-plugins/security
agy plugin install ~/agy-plugins/code-review
agy plugin list
```

### Opción B — Ya las tenías en Gemini CLI

Si instalaste las extensiones con `gemini extensions install ...`, impórtalas (igual en PowerShell y Bash):
```bash
agy plugin import gemini
agy plugin list
```

### Verificación

Abre `agy` y escribe `/skills`. Debes ver las skills de ambos plugins:

| Plugin | Skill / comando | Para qué sirve |
|---|---|---|
| security | `/security:analyze` | Analiza los cambios de la rama actual en busca de vulnerabilidades |
| security | `/security:scan-deps` | Revisa las dependencias contra la base de datos [OSV.dev](https://osv.dev/) |
| code-review | `/code-review` | Revisa la calidad de los cambios de la rama actual |
| code-review | `/pr-code-review` | Revisa un Pull Request (requiere el MCP de GitHub) |

> [!NOTE]
> Al importar, los comandos de las extensiones se convierten en skills. Si en tu versión aparecen con otro nombre (por ejemplo `/security-analyze`), usa el que muestre `/skills`. También puedes invocarlas en lenguaje natural: *"usa la skill de security para..."*.

---

## 🛡️ Paso 5: Análisis de seguridad interactivo

Asegúrate de estar en la rama del refactor y abre `agy`:
```bash
git checkout refactor/analysis-demo
agy
```

Lanza el análisis:
```text
/security:analyze
```

`agy` te pedirá permiso para leer archivos y ejecutar comandos de `git`. Revisa cada solicitud y apruébala (o elige *permitir siempre* para los comandos de solo lectura). El plugin trabaja por etapas y guarda su avance en la carpeta `.gemini_security/`.

Cuando termine, pídele que guarde el resultado:
```text
Escribe el resultado completo en security-analysis.md, en español, con una tabla resumen ordenada por severidad.
```

Ahora escanea las dependencias:
```text
/security:scan-deps
```

> [!TIP]
> Puedes acotar el análisis con lenguaje natural, por ejemplo: `/security:analyze enfócate solo en inyección SQL y SSRF en main.py`.

**¿Qué deberías encontrar?** Inyecciones SQL, un SSRF, un endpoint que expone las variables de entorno, CORS abierto con credenciales, *mass assignment* y una dependencia con CVEs. El instructor tiene la lista completa en [`guia_instructor/hallazgos_esperados.md`](guia_instructor/hallazgos_esperados.md): **no la veas antes de terminar** 😉.

---

## 🤖 Paso 6: Revisión de código en modo headless

En el modo headless `agy` ejecuta un solo prompt y termina, ideal para scripts y CI. El codelab original usa `--yolo`; en `agy` el equivalente es `--dangerously-skip-permissions`.

> [!WARNING]
> `--dangerously-skip-permissions` aprueba **todo** sin preguntar. Úsalo solo en repositorios de práctica o dentro de un contenedor/CI desechable. Alternativa más segura: agrega `--sandbox`.

### 1. (Opcional) Crear una guía de revisión para el equipo

#### En Windows (PowerShell):
```powershell
agy -p "Crea una guía completa de buenas prácticas de revisión de código para revisores (en español) y escríbela en GEMINI.md" `
  --dangerously-skip-permissions
```

#### En Linux o macOS:
```bash
agy -p "Crea una guía completa de buenas prácticas de revisión de código para revisores (en español) y escríbela en GEMINI.md" \
  --dangerously-skip-permissions
```

`agy` lee `GEMINI.md` y `AGENTS.md` automáticamente, así que la revisión siguiente seguirá esas reglas.

### 2. Ejecutar la revisión de código

#### En Windows (PowerShell):
```powershell
agy -p "Activa la skill de code-review, revisa los cambios de la rama actual contra main y escribe el resultado en code-review.md" `
  --dangerously-skip-permissions `
  --print-timeout 15m
```

#### En Linux o macOS:
```bash
agy -p "Activa la skill de code-review, revisa los cambios de la rama actual contra main y escribe el resultado en code-review.md" \
  --dangerously-skip-permissions \
  --print-timeout 15m
```

### 3. Revisar los reportes

#### En Windows (PowerShell):
```powershell
Get-Content code-review.md
Get-Content security-analysis.md
```

#### En Linux o macOS:
```bash
cat code-review.md
cat security-analysis.md
```

> [!TIP]
> Para integrarlo con otras herramientas, pide la salida en JSON: `agy -p "..." --output-format json`. El resultado trae los campos `status` y `response`.

---

## 🐙 Paso 7: Servidor MCP de GitHub y comentario en el Pull Request

Con el **Model Context Protocol (MCP)**, `agy` puede leer y comentar Pull Requests en GitHub.

### 1. Publicar el repositorio y abrir un Pull Request

#### En Windows (PowerShell):
```powershell
gh auth login
git checkout main
gh repo create inventario-api --private --source . --push
git checkout refactor/analysis-demo
git push -u origin refactor/analysis-demo
gh pr create --base main --title "Refactor: nuevos endpoints" --body "PR de práctica para el taller de análisis de código."
```

#### En Linux o macOS:
```bash
gh auth login
git checkout main
gh repo create inventario-api --private --source . --push
git checkout refactor/analysis-demo
git push -u origin refactor/analysis-demo
gh pr create --base main --title "Refactor: nuevos endpoints" --body "PR de práctica para el taller de análisis de código."
```

### 2. Crear un token de acceso personal (PAT)

1. En GitHub ve a **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. En *Repository access* elige **Only select repositories → inventario-api**.
3. Permisos: **Pull requests: Read and write** y **Contents: Read-only**.
4. Copia el token (empieza con `github_pat_...`).

> [!NOTE]
> El codelab original usa un token *classic* con el permiso `repo`. Un token *fine-grained* limitado a un solo repositorio es más seguro y funciona igual.

### 3. Configurar el servidor MCP de GitHub

Puedes configurarlo directamente con el comando de terminal de `agy` (más rápido) o creando el archivo JSON de configuración.

#### Método 1 — Con comando directo de `agy` (Recomendado):

Tanto en PowerShell como en Bash, desde la carpeta `inventario-api`:
```bash
agy mcp add --header "Authorization: Bearer github_pat_TU_TOKEN_AQUI" github https://api.githubcopilot.com/mcp/
```

#### Método 2 — Mediante archivo `.agents/mcp_config.json`:

En `agy` los servidores MCP también pueden residir en `.agents/mcp_config.json` (ya está en `.gitignore`).

##### En Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force -Path .agents | Out-Null
Copy-Item "$HOME\codelab-code-analysis-antigravity\plantillas\mcp_config.json" .agents\mcp_config.json
notepad .agents\mcp_config.json
```

##### En Linux o macOS:
```bash
mkdir -p .agents
cp ~/codelab-code-analysis-antigravity/plantillas/mcp_config.json .agents/mcp_config.json
nano .agents/mcp_config.json
```

Reemplaza el token en el archivo:
```json
{
  "mcpServers": {
    "github": {
      "serverUrl": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer github_pat_TU_TOKEN_AQUI"
      }
    }
  }
}
```

> [!CAUTION]
> Este archivo contiene tu token. Verifica con `git status` que **no** aparezca para commit.

### 4. Verificar y usar el MCP

Abre `agy`, escribe `/mcp` y confirma que el servidor `github` aparece **conectado** con sus herramientas. Luego:

```text
Une los hallazgos de @code-review.md y @security-analysis.md en un solo reporte en español, sin hallazgos duplicados y ordenado por severidad. Publica ese reporte como comentario en el Pull Request abierto de la rama actual en GitHub y muéstrame la URL del PR para revisarlo manualmente.
```

`agy` te pedirá permiso antes de escribir en GitHub. Abre la URL y revisa el comentario. También puedes probar la skill de PR:
```text
/pr-code-review
```

---

## ⚙️ Paso 8: Automatizar en CI/CD con GitHub Actions

Ahora hacemos que cada Pull Request se revise solo. La plantilla [`plantillas/revision-agy.yml`](plantillas/revision-agy.yml) instala `agy`, instala los dos plugins, ejecuta la revisión en modo headless y publica el reporte como comentario con `gh`.

### 1. Crear el secreto con tu API Key

#### En Windows (PowerShell):
```powershell
gh secret set GEMINI_API_KEY --body "tu-api-key-aqui"
```

#### En Linux o macOS:
```bash
gh secret set GEMINI_API_KEY --body "tu-api-key-aqui"
```

### 2. Agregar el workflow a la rama del refactor

#### En Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force -Path .github\workflows | Out-Null
Copy-Item "$HOME\codelab-code-analysis-antigravity\plantillas\revision-agy.yml" .github\workflows\revision-agy.yml
git add .github
git commit -m "ci: revisión automática con Antigravity CLI"
git push
```

#### En Linux o macOS:
```bash
mkdir -p .github/workflows
cp ~/codelab-code-analysis-antigravity/plantillas/revision-agy.yml .github/workflows/revision-agy.yml
git add .github
git commit -m "ci: revisión automática con Antigravity CLI"
git push
```

El `push` actualiza el PR (evento `synchronize`) y dispara el workflow. Síguelo con:
```bash
gh run watch
```

Fragmento clave del workflow:
```yaml
- name: Ejecutar la revisión en modo headless
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    BASE_REF: ${{ github.base_ref }}
  run: |
    agy -p "Usa las skills de code-review y security para revisar SOLO los cambios de git diff origin/${BASE_REF}...HEAD ..." \
      --dangerously-skip-permissions \
      --print-timeout 15m
```

> [!NOTE]
> **Alternativa oficial:** Google mantiene la acción [`google-github-actions/run-gemini-cli`](https://github.com/google-github-actions/run-gemini-cli), que usa Gemini CLI, y el plugin de seguridad incluye un [workflow listo](https://github.com/gemini-cli-extensions/security/blob/main/.github/workflows/gemini-review.yml). Es la opción que usa el codelab original y sigue siendo útil en organizaciones con Gemini Code Assist o Vertex AI.

---

## 🩹 Paso 9 (Bonus): Remediación asistida

Encontrar vulnerabilidades es la mitad del trabajo. Pídele a `agy` que las corrija en una rama nueva:

```bash
git checkout -b fix/vulnerabilidades
agy
```

```text
/plan
Con base en @security-analysis.md, corrige todas las vulnerabilidades de severidad Crítica y Alta en main.py:
- Usa consultas parametrizadas o el ORM de SQLAlchemy en lugar de f-strings.
- Elimina /debug/env/ y /admin/fetch-url/ (o protégelos con autenticación y lista blanca de dominios).
- Usa un esquema Pydantic en /products/bulk-update/.
- Restringe CORS y desactiva debug.
Explícame cada cambio antes de aplicarlo.
```

Después vuelve a ejecutar el análisis y compara:
```text
/security:analyze
Compara el resultado con @security-analysis.md y dime qué hallazgos quedaron resueltos y cuáles siguen abiertos.
```

---

## 🧪 Plan B: Google Cloud Shell

Si no puedes instalar nada en tu equipo, usa [Google Cloud Shell](https://shell.cloud.google.com/) (terminal Linux gratuita en el navegador, con `git`, `python3` y `gh` preinstalados):

1. Abre [shell.cloud.google.com](https://shell.cloud.google.com/) e inicia sesión con tu cuenta de Google.
2. Sigue todos los pasos usando los comandos de **Linux / macOS (Bash)**.
3. Para abrir archivos en el editor: `cloudshell edit code-review.md`.
4. Para iniciar sesión en `agy` desde Cloud Shell, copia la URL que te muestra en otra pestaña e ingresa el código de confirmación.

---

## 🧹 Limpieza de Recursos

#### En Windows (PowerShell):
```powershell
# Borrar el repositorio de práctica en GitHub (pide confirmación)
gh repo delete inventario-api

# Borrar la carpeta local y los plugins
Remove-Item -Recurse -Force "$HOME\inventario-api"
agy plugin uninstall security
agy plugin uninstall code-review
```

#### En Linux o macOS:
```bash
# Borrar el repositorio de práctica en GitHub (pide confirmación)
gh repo delete inventario-api

# Borrar la carpeta local y los plugins
rm -rf ~/inventario-api
agy plugin uninstall security
agy plugin uninstall code-review
```

Finalmente, **revoca el token** en GitHub (**Settings → Developer settings → Personal access tokens**) y, si creaste una API Key solo para el taller, bórrala en [Google AI Studio](https://aistudio.google.com/apikey).

> [!NOTE]
> `gh repo delete` requiere el permiso `delete_repo`. Si falla, ejecuta `gh auth refresh -s delete_repo` o bórralo desde **Settings → Danger Zone** del repositorio.

---

## 🩺 Solución de Problemas

<details>
<summary><b>🪟 <code>agy</code> no se reconoce como comando</b></summary>

Cierra y vuelve a abrir la terminal para que tome el nuevo `PATH`. Si persiste, reinstala:

- 🪟 PowerShell: `irm https://antigravity.google/cli/install.ps1 | iex`
- 🐧 Bash: `curl -fsSL https://antigravity.google/cli/install.sh | bash` y luego `source ~/.bashrc`
</details>

<details>
<summary><b>🪟 <code>preparar_repo.ps1 no se puede cargar porque la ejecución de scripts está deshabilitada</code></b></summary>

Permite scripts solo en la ventana actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\preparar_repo.ps1
```
</details>

<details>
<summary><b><code>La carpeta ... ya existe</code> al preparar el repositorio</b></summary>

Ya habías corrido el script. Bórrala o usa otra ruta:

- 🪟 PowerShell: `.\scripts\preparar_repo.ps1 -Destino "$HOME\inventario-api-2"`
- 🐧 Bash: `bash scripts/preparar_repo.sh ~/inventario-api-2`
</details>

<details>
<summary><b>No aparecen las skills <code>security</code> o <code>code-review</code> en <code>/skills</code></b></summary>

1. Ejecuta `agy plugin list` y confirma que ambos plugins estén **habilitados** (si no: `agy plugin enable security`).
2. Valida el plugin: `agy plugin validate security`.
3. Sal de `agy` con `/quit` y vuelve a entrar para recargar.
4. Si vienes de Gemini CLI, prueba la Opción B: `agy plugin import gemini`.
</details>

<details>
<summary><b>El análisis dice que no hay cambios que revisar</b></summary>

Estás en la rama `main`. Cambia a la rama del refactor: `git checkout refactor/analysis-demo` y confirma con `git diff --stat main...HEAD`.
</details>

<details>
<summary><b>Error de autenticación o <code>API key not valid</code></b></summary>

Revisa que `settings.json` tenga `"modelProvider": "gemini"` y que la variable exista en la sesión actual:

- 🪟 PowerShell: `$env:GEMINI_API_KEY = "AIzaSy...tu-clave"`
- 🐧 Bash: `export GEMINI_API_KEY="AIzaSy...tu-clave"`

Para dejarla fija en Windows: `[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIzaSy...", "User")`. En Linux agrégala a `~/.bashrc`.
</details>

<details>
<summary><b><code>/mcp</code> muestra el servidor de GitHub desconectado</b></summary>

- El archivo debe estar en `.agents/mcp_config.json` **dentro** de `inventario-api` y usar la clave `serverUrl` (no `httpUrl`, que era de Gemini CLI).
- El header debe ser `"Authorization": "Bearer <token>"`.
- Verifica que el token no haya expirado y tenga permiso sobre el repositorio `inventario-api`.
- Recarga desde el mismo `/mcp` o reinicia `agy`.
</details>

<details>
<summary><b>El modo headless se queda esperando o se corta</b></summary>

- Sin `--dangerously-skip-permissions`, `agy -p` no puede pedirte aprobaciones y se detiene.
- El tiempo máximo por defecto es 5 minutos; auméntalo con `--print-timeout 15m`.
</details>

<details>
<summary><b>El workflow de GitHub Actions no comenta en el PR</b></summary>

- Confirma que existe el secreto `GEMINI_API_KEY`: `gh secret list`.
- En **Settings → Actions → General → Workflow permissions** habilita **Read and write permissions**.
- Revisa el log del paso *Ejecutar la revisión*: `gh run view --log-failed`.
</details>

<details>
<summary><b>🪟 <code>uv sync</code> falla al instalar <code>requests==2.19.1</code></b></summary>

Es la dependencia vulnerable "a propósito" para `/security:scan-deps`. Ejecutar la API es opcional; si solo quieres levantarla, cámbiate a `main` (`git checkout main`) y ahí ejecuta `uv sync`.
</details>

<details>
<summary><b>Error de plugins o hooks: <code>Cannot find module ... telemetry_hook_bundle.js</code> o fallo en <code>PreToolUse</code></b></summary>

Si un plugin antiguo (como `datacloud_telemetry`) tiene rutas rotas en Windows o comillas literales incorrectas, bloqueará la ejecución de cualquier herramienta en el agente.

Para solucionarlo, elimina la carpeta del plugin problemático en PowerShell:

```powershell
Remove-Item -Recurse -Force "$HOME\.gemini\config\plugins\googlecloudtools.datacloud_telemetry*"
```
*(O en Bash: `rm -rf ~/.gemini/config/plugins/googlecloudtools.datacloud_telemetry*`)*
</details>

<details>
<summary><b>Git: <code>Author identity unknown</code> o <code>fatal: empty ident name</code> al hacer commit</b></summary>

Git no tiene configurado tu usuario en la máquina. Configúralo globalmente ejecutando:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```
</details>

<details>
<summary><b><code>fatal: destination path '...' already exists</code> al clonar plugins</b></summary>

Ocurre si intentas clonar nuevamente en una carpeta que ya existe. Elimínala y vuelve a clonar:

- 🪟 PowerShell: `Remove-Item -Recurse -Force "$HOME\agy-plugins"`
- 🐧 Bash: `rm -rf ~/agy-plugins`
</details>

<details>
<summary><b><code>gh repo create: Name already exists on this account</code></b></summary>

Ya tienes un repositorio con el nombre `inventario-api` en tu cuenta de GitHub. Puedes eliminar el repositorio anterior con:

```bash
gh repo delete inventario-api --yes
```

O si prefieres conservarlo, crea uno con otro nombre (por ejemplo `inventario-api-demo`):
```bash
gh repo create inventario-api-demo --private --source . --push
```
</details>

---

## 📚 Recursos para Seguir Aprendiendo

* 🚀 **[Antigravity CLI – Instalación](https://antigravity.google/docs/cli/install/)**: instalación, autenticación y primeros pasos.
* 🔄 **[Migración desde Gemini CLI](https://antigravity.google/docs/cli/gcli-migration/)**: extensiones → plugins, MCP y skills.
* 🧠 **[Skills](https://antigravity.google/docs/skills/)** y **[MCP](https://antigravity.google/docs/mcp/)** en Antigravity.
* 🤖 **[Modo headless](https://antigravity.google/docs/cli/headless/)**: flags para scripts y CI.
* 🧪 **[Codelab: Hands-on with Antigravity CLI](https://codelabs.developers.google.com/antigravity-cli-hands-on)**.
* 🛡️ **[Plugin Security](https://github.com/gemini-cli-extensions/security)** y **[Plugin Code Review](https://github.com/gemini-cli-extensions/code-review)**.
* 🐙 **[GitHub MCP Server](https://github.com/github/github-mcp-server)**: herramientas disponibles y permisos.
* ⚙️ **[run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli)**: GitHub Action oficial de Google.
* 🔐 **[OWASP Top 10](https://owasp.org/Top10/)** y **[OSV.dev](https://osv.dev/)**: vulnerabilidades web y base de datos de CVEs.
* 📘 **[Codelab original (español)](https://codelabs.developers.google.com/gemini-cli-code-analysis?hl=es-419)**.

---

<p align="center">
  <b>Powered by aaronthewarrior</b> • Construido con ❤️ para la comunidad de desarrolladores<br><br>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" width="16" height="16" align="center" /> <a href="https://me.developers.google.com/u/108177037637693690075">Google Developer Expert</a> &nbsp;•&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="16" height="16" align="center" /> <a href="https://github.com/aaron-the-warrior">aaron-the-warrior</a> &nbsp;•&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="16" height="16" align="center" /> <a href="https://www.linkedin.com/in/aaronthewarrior/">aaronthewarrior</a> &nbsp;•&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/twitter/twitter-original.svg" width="16" height="16" align="center" /> <a href="https://twitter.com/aaronthewarrior">@aaronthewarrior</a> &nbsp;•&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg" width="16" height="16" align="center" /> <a href="https://www.facebook.com/aaron.guerrero.hernandez">Facebook</a>
</p>
