"""
Embeddings service for document processing
"""

import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Try to use new langchain-huggingface package, fallback to deprecated one
try:
    from langchain_huggingface import HuggingFaceEmbeddings

    logger.info("Using langchain-huggingface package")
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings

        logger.warning(
            "Using deprecated HuggingFaceEmbeddings. Install langchain-huggingface for better support: pip install langchain-huggingface"
        )
    except ImportError:
        raise ImportError(
            "HuggingFaceEmbeddings not found. Install with: "
            "pip install langchain-huggingface or pip install langchain-community"
        )


class EmbeddingsService:
    """Service for managing embeddings."""

    def __init__(self):
        """Initialize embeddings service."""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL, model_kwargs={"device": settings.EMBEDDING_DEVICE}
            )
            logger.info(f"Embeddings initialized: {settings.EMBEDDING_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise

    def get_embeddings(self):
        """Get the embeddings model."""
        return self.embeddings


# Global embeddings service instance
embeddings_service = EmbeddingsService()
