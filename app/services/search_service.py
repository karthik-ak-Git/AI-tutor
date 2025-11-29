"""
Web search service using DuckDuckGo
"""

import logging

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from app.config import settings

logger = logging.getLogger(__name__)


class SearchService:
    """Service for web search operations."""

    def __init__(self):
        """Initialize search service."""
        try:
            wrapper = DuckDuckGoSearchAPIWrapper(max_results=settings.SEARCH_MAX_RESULTS)
            self.search_tool = DuckDuckGoSearchResults(api_wrapper=wrapper)
            logger.info("Web search tool initialized (DuckDuckGo)")
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            raise

    def search(self, query: str) -> str:
        """Perform web search."""
        try:
            result = self.search_tool.invoke(query)
            return result
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return f"Error performing search: {str(e)}"

    def get_tool(self):
        """Get the search tool."""
        return self.search_tool


# Global search service instance
search_service = SearchService()

