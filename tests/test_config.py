from anime_shop.config import Settings


def test_defaults_without_env_file(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    settings = Settings(_env_file=None)
    assert settings.llm_provider == "anthropic"
    assert settings.claude_model == "claude-opus-5-5"
    assert settings.database_url.startswith("sqlite:///")


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_CHAT_MODEL", "qwen2.5:3b")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    settings = Settings(_env_file=None)
    assert settings.llm_provider == "ollama"
    assert settings.ollama_chat_model == "qwen2.5:3b"
    # La key nunca se imprime en logs/reprs.
    assert "sk-test" not in repr(settings)


def test_empty_api_key_is_treated_as_missing(monkeypatch):
    # Caso real: el .env trae "ANTHROPIC_API_KEY=" sin valor.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "  ")
    settings = Settings(_env_file=None)
    assert settings.anthropic_api_key is None
    assert settings.langfuse_secret_key is None
