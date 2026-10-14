#!/usr/bin/env bash
# Instalación del entorno en macOS Apple Silicon (M1/M2/M3).
# Uso: bash scripts/setup_mac.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ "$(uname -s)" != "Darwin" || "$(uname -m)" != "arm64" ]]; then
  echo "Este script está pensado para macOS en Apple Silicon (arm64)." >&2
  exit 1
fi

echo "==> 1/5 Homebrew"
if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

echo "==> 2/5 uv (gestor de Python y dependencias)"
command -v uv >/dev/null 2>&1 || brew install uv

echo "==> 3/5 Ollama (app nativa: usa la GPU del M1 vía Metal)"
if ! command -v ollama >/dev/null 2>&1; then
  brew install --cask ollama
fi
# Arranca el servidor si no está corriendo.
if ! curl -sf http://localhost:11434/api/version >/dev/null; then
  open -a Ollama || (ollama serve >/dev/null 2>&1 &)
  sleep 5
fi

echo "==> 4/5 Modelos locales (~2.3 GB en total)"
ollama pull llama3.2:3b        # LLM local de 3B (~2.0 GB), cabe en 8 GB de RAM
ollama pull nomic-embed-text   # Embeddings (~270 MB)

echo "==> 5/5 Entorno Python 3.12 + dependencias"
uv python install 3.12
uv sync --all-extras

[[ -f .env ]] || cp .env.example .env

echo
echo "Listo. Próximos pasos:"
echo "  1. Edita .env y pon tu ANTHROPIC_API_KEY"
echo "  2. uv run python scripts/check_env.py"
