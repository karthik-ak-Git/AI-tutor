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
            # Get API key from environment (never hardcoded)
            api_key = settings.OPENROUTER_API_KEY

            if not api_key or api_key.strip() == "":
                raise ValueError(
                    "OPENROUTER_API_KEY is not set. "
                    "Please set it in your .env file or environment variables."
                )

            # Validate API key format (should start with sk-)
            if not api_key.startswith("sk-"):
                logger.warning(
                    "API key format may be incorrect. "
                    "OpenRouter API keys typically start with 'sk-'"
                )

            self.llm = ChatOpenAI(
                model=settings.OPENROUTER_MODEL,
                openai_api_key=api_key,  # From environment only
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=settings.OPENROUTER_TEMPERATURE,
                timeout=settings.OPENROUTER_TIMEOUT,
            )
            logger.info(f"LLM initialized: {settings.OPENROUTER_MODEL}")
            logger.debug("API key loaded from environment (not hardcoded)")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
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
