# Anime Shop Agents

Sistema multi-agente que administra una tienda web de compra y venta de figuras de anime
(Nendoroid, Figma, scale figures, etc.). Es un proyecto de portafolio para puestos de
**AI Engineer / Data AI Engineer**: cubre agentes con LLMs, tool use, RAG, orquestación,
evaluación, observabilidad y un backend real.

> Fase actual: **0. Entorno**. El código de los agentes se construye en las siguientes fases.

---

## 1. Decisiones de stack (y por qué)

Restricción: **MacBook M1 con 8 GB de RAM**. Todo se eligió para que corra sin Docker y
dejando memoria libre para el navegador y el IDE.

| Capa | Herramienta | Por qué | Concepto que demuestra |
|---|---|---|---|
| Python y dependencias | **uv** + Python 3.12 | 10-100x más rápido que pip/poetry, lockfile reproducible | Reproducibilidad |
| LLM principal | **Claude API** (`anthropic`) | Tool use y razonamiento de primer nivel; no consume RAM local | Tool use, structured outputs, prompt caching |
| LLM local | **Ollama** + `llama3.2:3b` | Gratis y offline; corre en la GPU del M1 vía Metal | Trade-offs costo/calidad/latencia, model routing |
| Embeddings | **Ollama** + `nomic-embed-text` | ~270 MB, sin instalar PyTorch (que pesa GBs) | Embeddings, búsqueda semántica |
| Orquestación | **LangGraph** | Agentes como grafo de estados, checkpoints, human-in-the-loop | Arquitecturas multi-agente (supervisor, router) |
| Herramientas | **MCP** (`mcp`) | Estándar abierto para exponer herramientas a LLMs | Interoperabilidad de agentes |
| Vector DB | **Qdrant** en modo local | API de producción, pero embebido en disco (sin servidor) | RAG, filtros por metadatos |
| Backend | **FastAPI** + **SQLModel** + SQLite | API tipada y async; SQLite = cero RAM extra | Integración de agentes con sistemas reales |
| Datos/ML | **pandas**, **DuckDB**, **scikit-learn** | Analítica y modelos clásicos (pricing, anomalías) | Data engineering + ML clásico junto a LLMs |
| UI | **Streamlit** | Chat y dashboard en minutos | Demo para entrevistas |
| Observabilidad | **structlog** + **Langfuse** (opcional) | Trazas, costos y latencias por llamada | LLMOps |
| Calidad | **pytest**, **ruff**, **mypy**, **pre-commit** | Estándar de la industria | Ingeniería de software |

### Presupuesto de memoria (8 GB)

| Proceso | RAM aprox. |
|---|---|
| macOS + navegador + VS Code | ~4.5 GB |
| Ollama con `llama3.2:3b` cargado | ~2.5 GB (se descarga solo tras 5 min sin uso) |
| Python (FastAPI + Qdrant local + Streamlit) | ~0.5 GB |

Por eso **Claude es el proveedor por defecto** y Ollama es el de respaldo/experimentación.
Evita modelos locales de 7B+ y Docker Desktop: no caben cómodamente.

---

## 2. Instalación (macOS Apple Silicon)

### Clonar

```bash
git clone https://github.com/<tu-usuario>/anime-shop-agents.git
cd anime-shop-agents
```

### Opción A: automática

```bash
bash scripts/setup_mac.sh      # o: make setup
```

### Opción B: paso a paso (recomendado para aprender)

```bash
# 1. Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. uv: gestiona versiones de Python, venvs y dependencias
brew install uv

# 3. Ollama: usa la app NATIVA (no Docker) para tener aceleración Metal
brew install --cask ollama
open -a Ollama
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# 4. Python 3.12 + todas las dependencias (crea .venv/ e instala desde uv.lock)
uv python install 3.12
uv sync --all-extras

# 5. Variables de entorno
cp .env.example .env
# edita .env y pega tu ANTHROPIC_API_KEY (https://console.anthropic.com/settings/keys)
```

### Verificación

```bash
make check-offline   # solo librerías
make check           # librerías + Ollama + una llamada mínima a Claude
make test            # tests unitarios
```

Deberías ver una tabla con todo en `OK`. Si algo falla, la columna *Detalle* dice qué hacer.

### Editor

VS Code con las extensiones *Python*, *Ruff* y *Jupyter*. Selecciona el intérprete
`.venv/bin/python` (Cmd+Shift+P -> "Python: Select Interpreter").

---

## 3. Estructura

```
anime-shop-agents/
├── pyproject.toml        # dependencias y configuración de herramientas
├── uv.lock               # versiones exactas (reproducible en cualquier Mac)
├── .env.example          # plantilla de configuración
├── Makefile              # atajos: setup, check, test, lint
├── scripts/
│   ├── setup_mac.sh      # instalación automática
│   └── check_env.py      # verificación del entorno
├── src/anime_shop/
│   └── config.py         # Settings tipados (pydantic-settings)
├── tests/
├── data/                 # SQLite, Qdrant local, datasets (ignorado en git)
└── notebooks/            # exploración
```

---

## 4. Hoja de ruta

| Fase | Contenido | Conceptos clave para la entrevista |
|---|---|---|
| **0. Entorno** ✅ | Dependencias, config, verificación | Reproducibilidad, gestión de secretos |
| 1. Dominio y datos | Modelo de datos (figuras, usuarios, órdenes, ofertas), dataset sintético, API FastAPI | Data modeling, ETL, DuckDB |
| 2. Primer agente | Agente de catálogo con tool use (buscar, crear listing) | Tool use, structured outputs, loop agéntico |
| 3. RAG | Búsqueda semántica de figuras + FAQ/políticas | Chunking, embeddings, retrieval híbrido, re-ranking |
| 4. Multi-agente | Supervisor + agentes: Catálogo, Precios, Atención al cliente, Moderación/fraude, Inventario | Patrones supervisor/router, estado compartido, human-in-the-loop |
| 5. ML clásico | Sugerencia de precio, detección de listings sospechosos | Feature engineering, cuándo NO usar un LLM |
| 6. Evaluación | Dataset de evals, LLM-as-judge, métricas de RAG | Evals, regresiones, hill-climbing de prompts |
| 7. Observabilidad y costos | Trazas, tokens, latencia, prompt caching, routing Claude/Ollama | LLMOps, optimización de costos |
| 8. Seguridad | Prompt injection en listings de usuarios, guardrails, PII | AI safety aplicada |
| 9. MCP + UI + deploy | Servidor MCP de la tienda, chat Streamlit, CI con GitHub Actions | Interoperabilidad, CI/CD |
