"""
Tests for configuration management
"""
import pytest
import os
from app.config import Settings


def test_settings_loads_from_env(monkeypatch):
    """Test that settings load from environment variables."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-123")
    settings = Settings()
    assert settings.OPENROUTER_API_KEY == "test-key-123"
    assert settings.OPENROUTER_MODEL == "openai/gpt-4.1-nano"


def test_settings_defaults():
    """Test that settings have correct defaults."""
    os.environ["OPENROUTER_API_KEY"] = "test-key"
    settings = Settings()
    assert settings.API_VERSION == "1.0.0"
    assert settings.CHUNK_SIZE == 1000
    assert settings.RETRIEVER_K == 4
    assert settings.LOG_LEVEL == "INFO"


def test_port_property():
    """Test port property reads from environment."""
    os.environ["OPENROUTER_API_KEY"] = "test-key"
    os.environ["PORT"] = "9000"
    settings = Settings()
    assert settings.port == 9000
    del os.environ["PORT"]



