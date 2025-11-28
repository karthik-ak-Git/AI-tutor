"""
LLM service for OpenAI/OpenRouter integration
"""

from langchain_openai import ChatOpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for managing LLM interactions."""

    def __init__(self):
        """Initialize LLM service."""
        try:
            self.llm = ChatOpenAI(
                model=settings.OPENROUTER_MODEL,
                openai_api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=settings.OPENROUTER_TEMPERATURE,
                timeout=settings.OPENROUTER_TIMEOUT,
            )
            logger.info(f"LLM initialized: {settings.OPENROUTER_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    def invoke(self, prompt: str):
        """Invoke LLM with a prompt."""
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            raise

    @property
    def model_name(self) -> str:
        """Get the model name."""
        return settings.OPENROUTER_MODEL


# Global LLM service instance
llm_service = LLMService()
