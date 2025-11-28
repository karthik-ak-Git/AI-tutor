"""
Configuration management for AI Tutor application
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_TITLE: str = "AI Tutor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI Tutor & Research Agent API with RAG and Web Search"

    # OpenRouter Configuration
    # API key must be provided via environment variable or .env file
    # Never hardcode API keys in the source code
    OPENROUTER_API_KEY: str  # Required - must be set in environment (.env file)
    OPENROUTER_MODEL: str = "openai/gpt-4.1-nano"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_TEMPERATURE: float = 0.5
    OPENROUTER_TIMEOUT: int = 30

    # Embeddings Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"

    # RAG Configuration
    PDF_PATH: Optional[str] = None
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVER_K: int = 4
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    CHROMA_DB_PATH: str = "chroma_db"

    # Search Configuration
    SEARCH_MAX_RESULTS: int = 10

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Render/Production Configuration
    @property
    def port(self) -> int:
        """Get port from environment or default."""
        return int(os.getenv("PORT", self.PORT))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
