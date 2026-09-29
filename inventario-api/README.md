# API de Gestión de Inventario (demo vulnerable)

> [!CAUTION]
> Este repositorio contiene **código INTENCIONALMENTE VULNERABLE** con fines educativos.
> **NO lo despliegues en producción ni en servidores públicos.**

API en **FastAPI + SQLAlchemy + SQLite** para gestionar productos, inventario y transacciones. Se usa en el taller *Revisión de código y análisis de seguridad con Antigravity CLI* para practicar:

- Revisión de código asistida por IA (`code-review`).
- Análisis de seguridad (`security`) sobre los cambios de la rama `refactor/analysis-demo`.

La rama `refactor/analysis-demo` introduce a propósito vulnerabilidades del **OWASP Top 10**:

1. Control de acceso roto
2. Fallas criptográficas / exposición de información
3. Inyección (SQL)
4. Diseño inseguro
5. Configuración de seguridad incorrecta
6. Fallas de integridad de software y datos
7. Fallas de registro y monitoreo
8. Server-Side Request Forgery (SSRF)
9. *(Extra de esta adaptación)* Componentes vulnerables y desactualizados (`requests==2.19.1`)

## Ejecutar la API (opcional)

```bash
uv sync
uv run fastapi dev main.py
```

Documentación interactiva: `http://localhost:8000/docs`

---

Basado en [alphinside/gemini-cli-code-analysis-demo](https://github.com/alphinside/gemini-cli-code-analysis-demo) (Apache 2.0). Adaptación al español: **Powered by aaronthewarrior**.
