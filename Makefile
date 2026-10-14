.PHONY: setup install dev test lint format

setup:    ## Instalación completa en Mac (brew, uv, Python, dependencias)
	bash scripts/setup_mac.sh

install:  ## Solo dependencias de Python
	uv sync

dev:      ## Servidor de desarrollo con recarga automática en http://localhost:8000
	uv run uvicorn figure_store.main:app --reload

test:
	uv run pytest -q

lint:
	uv run ruff check . && uv run ruff format --check .

format:
	uv run ruff check --fix . && uv run ruff format .
