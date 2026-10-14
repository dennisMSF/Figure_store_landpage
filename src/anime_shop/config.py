"""Configuración central del proyecto, cargada desde variables de entorno / .env."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Proveedor de LLM ---
    # "anthropic": Claude en la nube (mejor calidad, tool use robusto).
    # "ollama": modelo local en la Mac (gratis, offline, menor calidad).
    llm_provider: Literal["anthropic", "ollama"] = "anthropic"

    anthropic_api_key: SecretStr | None = None
    # Modelo principal: razonamiento de los agentes orquestadores.
    claude_model: str = "claude-opus-5-5"
    # Modelo rápido/barato: clasificación, extracción y subtareas masivas.
    claude_fast_model: str = "claude-haiku-5-5"

    ollama_host: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.2:3b"
    ollama_embed_model: str = "nomic-embed-text"

    # --- Almacenamiento (todo local, sin Docker, pensado para 8 GB de RAM) ---
    database_url: str = f"sqlite:///{PROJECT_ROOT / 'data' / 'shop.db'}"
    qdrant_path: Path = PROJECT_ROOT / "data" / "qdrant"
    qdrant_collection: str = "figures"

    # --- Observabilidad (opcional) ---
    langfuse_public_key: str | None = None
    langfuse_secret_key: SecretStr | None = None
    langfuse_host: str = "https://cloud.langfuse.com"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    environment: Literal["dev", "test", "prod"] = Field(default="dev")

    @field_validator(
        "anthropic_api_key", "langfuse_public_key", "langfuse_secret_key", mode="before"
    )
    @classmethod
    def empty_str_to_none(cls, value: object) -> object:
        # En .env, "ANTHROPIC_API_KEY=" significa "no configurada", no una key vacía.
        if isinstance(value, str) and not value.strip():
            return None
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
