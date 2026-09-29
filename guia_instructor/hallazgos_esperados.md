# 🧑‍🏫 Guía del Instructor: Hallazgos Esperados

> **Powered by aaronthewarrior** · Material de apoyo para quien imparte el taller.

Esta es la "hoja de respuestas" de la rama `refactor/analysis-demo`. Úsala para validar que los reportes de Antigravity CLI (`code-review.md`, `security-analysis.md`) encontraron lo importante y para detectar **falsos negativos** o **falsos positivos**.

Todas las líneas se refieren a `main.py` en la rama `refactor/analysis-demo` (archivo `cambios_refactor/main.py` de esta carpeta).

---

## 🔴 Seguridad (lo que debe encontrar la skill `security`)

| # | Línea(s) | Endpoint | Vulnerabilidad | OWASP 2021 | Severidad |
|---|---|---|---|---|---|
| 1 | 432-445 | `POST /inventory/adjust-by-query/` | Inyección SQL: el cliente manda la cláusula `WHERE` completa (`sql_where`) y se concatena en un `UPDATE`. Permite modificar o borrar toda la tabla. | A03 Inyección | Crítica |
| 2 | 423-428 | `GET /debug/env/` | Expone **todas** las variables de entorno (`dict(os.environ)`): tokens, API Keys, contraseñas. | A05 Configuración incorrecta / A01 | Crítica |
| 3 | 260-273 | `GET /admin/fetch-url/` | **SSRF**: `requests.get(url)` con URL del usuario. Permite leer el servidor de metadatos de la nube (`169.254.169.254`) o servicios internos, y devuelve los headers. | A10 SSRF | Crítica |
| 4 | 96-105 | `GET /products/category/{category}` | Inyección SQL con f-string en `text()`. | A03 Inyección | Alta |
| 5 | 142-154 | `GET /products/search/` | Inyección SQL en `LIKE '%{query}%'` + devuelve el error y el traceback al cliente. | A03 / A05 | Alta |
| 6 | 368-380 | `GET /transactions/user/{user_name}` | Inyección SQL en `user_name`, `limit` y `skip`; el error de BD se devuelve en el `detail`. | A03 Inyección | Alta |
| 7 | 396-418 | `POST /products/bulk-update/` | *Mass assignment*: `setattr` sobre **cualquier** atributo (`id`, `created_at`...) sin esquema Pydantic ni autorización. | A04 Diseño inseguro / A08 Integridad | Alta |
| 8 | 383-393 | `GET /users/list/` | Endpoint sin autenticación que intenta listar usuarios (`SELECT * FROM users`). | A01 Control de acceso | Alta |
| 9 | 157-178 | `GET /products/export/` | Expone datos internos de negocio (`internal_cost`, `profit_margin`) sin autenticación. | A01 / A02 Exposición de datos | Media |
| 10 | 17-32 | Configuración de la app | `debug=True`, `/docs` y `/redoc` públicos, CORS `allow_origins=["*"]` **con** `allow_credentials=True`. | A05 Configuración incorrecta | Media |
| 11 | 451-461 | `GET /` | El health check revela versión de Python, modo debug y la ruta de la base de datos. | A05 Configuración incorrecta | Baja |
| 12 | Todos los endpoints admin/debug | — | Ningún endpoint tiene autenticación ni registro de auditoría (quién ajustó inventario, quién hizo bulk update). | A01 / A09 Registro y monitoreo | Media |
| 13 | `pyproject.toml` | Dependencias | `requests==2.19.1` tiene CVEs conocidos (p. ej. **CVE-2018-18074**, fuga de header `Authorization` en redirecciones). Lo detecta `/security:scan-deps` (OSV-Scanner). | A06 Componentes vulnerables | Media |

---

## 🟡 Calidad de código (lo que debe encontrar la skill `code-review`)

| # | Línea(s) | Hallazgo |
|---|---|---|
| 1 | 78, 85 | Se renombraron funciones a `GetProducts` / `GetProduct`: rompe la convención PEP 8 (`snake_case`) que sí sigue el resto del archivo. |
| 2 | 401 | **Bug**: `request.json()` es una corrutina en FastAPI/Starlette; sin `await` (y en una función síncrona) nunca devuelve el diccionario, así que el endpoint siempre falla. |
| 3 | 96-105 | El endpoint declara `response_model=List[ProductWithInventory]` pero devuelve filas crudas de SQL: la respuesta ya no incluye `inventory` y puede fallar la validación. |
| 4 | 158 | Parámetro `format` que no se usa (y además *sombrea* la función nativa `format`). |
| 5 | Varios | `except Exception` genérico que devuelve `{"error": ...}` con código **200**: el cliente no se entera del fallo. |
| 6 | 10 / `pyproject.toml` | Se agrega la dependencia `requests` solo para un endpoint; FastAPI ya trae `httpx`. |
| 7 | 459 | `os.sys.version` funciona por accidente; lo correcto es `import sys` y `sys.version`. |
| 8 | 112-121, 186-217 | `.dict()` está obsoleto en Pydantic v2; debe usarse `.model_dump()`. *(Existía desde `main`, puede aparecer o no.)* |
| 9 | `models.py` | `default=datetime.datetime.now(...)` se evalúa **una sola vez** al importar: todas las filas tienen la misma fecha. *(Existía desde `main`: si lo reporta, es un buen punto extra.)* |

---

## ✅ Criterios para evaluar el resultado en el taller

- **Mínimo esperado:** las 4 inyecciones SQL, el SSRF y `/debug/env/`.
- **Buen resultado:** además CORS/debug, mass assignment y la exposición de `internal_cost`.
- **Excelente:** detecta el bug de `request.json()` sin `await` y la dependencia vulnerable.
- Si aparecen hallazgos en archivos que **no** cambiaron, recuerda al grupo que las skills analizan el *diff* contra `main`: pídeles que revisen si el prompt pidió "todo el repositorio".

## 💬 Preguntas para la discusión final

1. ¿Qué hallazgos encontró una skill y no la otra? ¿Por qué tiene sentido tener ambas?
2. ¿Hubo falsos positivos? ¿Cómo lo decidiste?
3. ¿Qué parte del proceso automatizarías en CI y cuál dejarías siempre a una persona?
