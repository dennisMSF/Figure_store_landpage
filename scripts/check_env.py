"""Verifica que el entorno esté listo: librerías, Ollama local y acceso a Claude.

Uso:
    uv run python scripts/check_env.py            # chequeo completo
    uv run python scripts/check_env.py --offline  # sin llamadas de red (ni Ollama ni Claude)
"""

import argparse
import importlib
import platform
import sys

from rich.console import Console
from rich.table import Table

from anime_shop.config import get_settings

console = Console()

REQUIRED_MODULES = [
    "anthropic",
    "langgraph",
    "ollama",
    "mcp",
    "fastapi",
    "sqlmodel",
    "qdrant_client",
    "pandas",
    "duckdb",
    "sklearn",
    "streamlit",
    "structlog",
]


def check_system() -> list[tuple[str, bool, str]]:
    results = []
    py_ok = sys.version_info[:2] == (3, 12)
    results.append(("Python 3.12", py_ok, platform.python_version()))
    machine = platform.machine()
    results.append(("Arquitectura", True, f"{platform.system()} {machine}"))
    if platform.system() == "Darwin" and machine != "arm64":
        results.append(("Python nativo arm64", False, "Estás usando Python x86 (Rosetta)"))
    return results


def check_imports() -> list[tuple[str, bool, str]]:
    results = []
    for name in REQUIRED_MODULES:
        try:
            module = importlib.import_module(name)
            results.append((f"import {name}", True, getattr(module, "__version__", "ok")))
        except ImportError as exc:
            results.append((f"import {name}", False, str(exc)))
    return results


def check_ollama() -> list[tuple[str, bool, str]]:
    import ollama

    settings = get_settings()
    try:
        client = ollama.Client(host=settings.ollama_host)
        installed = {m.model for m in client.list().models}
    except Exception as exc:  # servidor caído, puerto incorrecto, etc.
        return [("Ollama servidor", False, f"{settings.ollama_host}: {exc}")]

    results = [("Ollama servidor", True, settings.ollama_host)]
    for wanted in (settings.ollama_chat_model, settings.ollama_embed_model):
        found = any(m == wanted or m.startswith(f"{wanted}:") for m in installed)
        detail = "descargado" if found else f"falta: ollama pull {wanted}"
        results.append((f"Modelo {wanted}", found, detail))

    if any(ok for _, ok, _ in results[1:]):
        try:
            emb = client.embed(model=settings.ollama_embed_model, input="Figura de Nendoroid")
            results.append(("Embeddings locales", True, f"dim={len(emb.embeddings[0])}"))
        except Exception as exc:
            results.append(("Embeddings locales", False, str(exc)))
    return results


def check_claude() -> list[tuple[str, bool, str]]:
    import anthropic

    settings = get_settings()
    if settings.anthropic_api_key is None:
        return [("Claude API", False, "ANTHROPIC_API_KEY vacía en .env")]

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    try:
        response = client.messages.create(
            model=settings.claude_fast_model,
            max_tokens=256,
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": "Responde solo con: listo"}],
        )
    except anthropic.AuthenticationError:
        return [("Claude API", False, "API key inválida")]
    except anthropic.RateLimitError:
        return [("Claude API", False, "Rate limit alcanzado, reintenta en un momento")]
    except anthropic.APIStatusError as exc:
        return [("Claude API", False, f"HTTP {exc.status_code}: {exc.message}")]
    except anthropic.APIConnectionError as exc:
        return [("Claude API", False, f"Sin conexión: {exc}")]

    if response.stop_reason == "refusal":
        return [("Claude API", False, "La petición fue rechazada (refusal)")]
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    return [("Claude API", True, f"{response.model} -> {text!r}")]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="omite Ollama y Claude")
    args = parser.parse_args()

    results = check_system() + check_imports()
    if not args.offline:
        results += check_ollama() + check_claude()

    table = Table(title="Anime Shop Agents - chequeo de entorno")
    table.add_column("Componente")
    table.add_column("Estado")
    table.add_column("Detalle")
    for name, ok, detail in results:
        table.add_row(name, "[green]OK[/]" if ok else "[red]FALLA[/]", detail)
    console.print(table)

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        console.print(f"[red]{len(failed)} componente(s) con problemas.[/]")
        return 1
    console.print("[green]Entorno listo.[/]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
