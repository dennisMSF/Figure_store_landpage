.PHONY: setup install check check-offline test lint format

setup:          ## Instalación completa en Mac M1 (brew, uv, ollama, modelos, deps)
	bash scripts/setup_mac.sh

install:        ## Solo dependencias de Python
	uv sync --all-extras

check:          ## Verifica librerías, Ollama y Claude
	uv run python scripts/check_env.py

check-offline:  ## Verifica solo librerías (sin red)
	uv run python scripts/check_env.py --offline

test:
	uv run pytest -q

lint:
	uv run ruff check . && uv run ruff format --check .

format:
	uv run ruff check --fix . && uv run ruff format .
