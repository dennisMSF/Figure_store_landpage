# Figure Store

Tienda web de figuras de anime **originales** con inventario propio.

Proyecto de aprendizaje y portafolio sobre cómo construir una web de comercio real desde cero
(backend, HTML, base de datos, pagos y despliegue), pensado para usarse de verdad más adelante.

> Fase actual: **0. Entorno + página de inicio**.

---

## Stack

Regla del proyecto: **cada dependencia entra cuando una función la necesita**, no antes.

| Pieza | Herramienta | Por qué |
|---|---|---|
| Python | **uv** + Python 3.12 | Instala Python y dependencias en segundos; `uv.lock` fija versiones exactas |
| Backend | **FastAPI** + **Uvicorn** | Framework moderno, tipado y con buena documentación |
| HTML | **Jinja2** (renderizado en el servidor) | Páginas que Google indexa bien (SEO), sin build de JavaScript |
| Estilos | **CSS propio** | Aprender los fundamentos (flexbox, grid, responsive) antes que un framework |
| Configuración | **pydantic-settings** + `.env` | Separar configuración y secretos del código |
| Calidad | **pytest** + **ruff** | Tests y linter estándar de la industria |

### ¿Y la IA?

Se evaluó y **se descartó por ahora**. En una tienda con inventario propio y catálogo pequeño,
el catálogo, carrito, pagos y envíos son software clásico: un LLM no mejora nada de eso y sí
agrega costo, latencia y fallos impredecibles. Se reconsiderará solo si aparece un problema
concreto que lo justifique (por ejemplo, búsqueda difícil con un catálogo grande).

---

## Instalación (macOS Apple Silicon)

```bash
git clone https://github.com/dennisMSF/Figure_store_landpage.git
cd Figure_store_landpage
bash scripts/setup_mac.sh   # o: make setup
make dev                    # abre http://localhost:8000
```

Otros comandos:

```bash
make test     # tests
make lint     # revisa estilo
make format   # corrige estilo automáticamente
```

Editor recomendado: VS Code con las extensiones *Python* y *Ruff*, usando el intérprete
`.venv/bin/python`.

---

## Estructura

```
Figure_store_landpage/
├── pyproject.toml              # dependencias y configuración de herramientas
├── uv.lock                     # versiones exactas
├── Makefile                    # atajos: setup, dev, test, lint
├── .env.example                # plantilla de configuración
├── scripts/setup_mac.sh        # instalación automática
├── src/figure_store/
│   ├── main.py                 # app FastAPI y rutas
│   ├── config.py               # configuración tipada
│   ├── templates/              # HTML (Jinja2)
│   └── static/css/             # estilos
└── tests/
```

---

## Hoja de ruta

| Fase | Contenido | Qué se aprende |
|---|---|---|
| **0. Entorno** ✅ | Proyecto, página de inicio, tests | Estructura de una app web, plantillas, CSS responsive |
| 1. Catálogo | Base de datos (SQLite + SQLModel), modelos de figura, páginas de listado y detalle, imágenes | Modelado de datos, ORM, rutas dinámicas |
| 2. Administración | Login de administrador, alta/edición de figuras y stock | Autenticación, formularios, validación |
| 3. Carrito y pedidos | Carrito, checkout, control de stock al comprar | Sesiones, transacciones, consistencia de datos |
| 4. Pagos | Stripe o Mercado Pago (según tu país), webhooks | Integración con APIs externas, seguridad |
| 5. Despliegue | Hosting, Postgres, dominio propio, HTTPS, CI con GitHub Actions | Producción, migraciones, variables de entorno |
| 6. Pulido | SEO, rendimiento, analítica, correos de confirmación | Lo que separa un proyecto de un producto |
