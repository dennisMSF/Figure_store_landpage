#!/usr/bin/env bash
# Instalación del entorno en macOS Apple Silicon.
# Uso: bash scripts/setup_mac.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> 1/3 Homebrew"
if ! command -v brew >/dev/null 2>&1; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

echo "==> 2/3 uv (gestor de Python y dependencias)"
command -v uv >/dev/null 2>&1 || brew install uv

echo "==> 3/3 Python 3.12 + dependencias"
uv python install 3.12
uv sync

[[ -f .env ]] || cp .env.example .env

echo
echo "Listo. Arranca la web con:  make dev   y abre http://localhost:8000"
