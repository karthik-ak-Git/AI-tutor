"""
Memory management for conversation context
"""

import logging
from typing import Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

logger = logging.getLogger(__name__)


class SimpleMemory:
    """Simple conversation memory that stores messages per session."""

    def __init__(self):
        """Initialize memory storage."""
        self.sessions: Dict[str, List[BaseMessage]] = {}
        logger.info("Memory service initialized")

    def add_user_message(self, session_id: str, content: str):
        """Add a user message to memory for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(HumanMessage(content=content))
        logger.debug(f"Added user message to session {session_id}")

    def add_ai_message(self, session_id: str, content: str):
        """Add an AI message to memory for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append(AIMessage(content=content))
        logger.debug(f"Added AI message to session {session_id}")

    def get_messages(self, session_id: str, last_n: Optional[int] = None) -> List[BaseMessage]:
        """Get messages for a session, optionally limited to last N."""
        messages = self.sessions.get(session_id, [])
        if last_n:
            return messages[-last_n:]
        return messages

    def clear_session(self, session_id: str):
        """Clear all messages for a specific session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session {session_id}")

    def clear_all(self):
        """Clear all sessions."""
        self.sessions.clear()
        logger.info("Cleared all sessions")
