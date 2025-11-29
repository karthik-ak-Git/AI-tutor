"""
Agent service that orchestrates LLM, RAG, and Search
"""

import logging

from langchain_core.runnables import RunnableLambda

from app.config import settings
from app.services.llm_service import llm_service
from app.services.memory import SimpleMemory
from app.services.rag_service import rag_service
from app.services.search_service import search_service

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing the AI agent."""

    def __init__(self):
        """Initialize agent service."""
        self.memory = SimpleMemory()
        self._initialize_tools()
        self.agent = RunnableLambda(self._agent_executor)
        logger.info(f"Agent initialized with {len(self.tools)} tools")

    def _initialize_tools(self):
        """Initialize tools (can be called to reload after document upload)."""
        self.retriever_tool = rag_service.get_retriever_tool()
        self.search_tool = search_service.get_tool()

        # Prepare tools list (only add non-None tools)
        self.tools = []
        if self.search_tool is not None:
            self.tools.append(self.search_tool)
        if self.retriever_tool is not None:
            self.tools.append(self.retriever_tool)

    def reload_tools(self):
        """Reload tools (useful after document upload)."""
        self._initialize_tools()
        logger.info("Tools reloaded")

    def _agent_executor(self, input_dict: dict) -> dict:
        """Simple agent that routes to appropriate tool."""
        query = input_dict.get("input", "")
        chat_history = input_dict.get("chat_history", [])
        use_document = input_dict.get("use_document", None)

        # Build context from chat history
        history_text = ""
        if chat_history:
            for msg in chat_history[-4:]:  # Last 4 messages for context
                if hasattr(msg, "content"):
                    role = "Human" if msg.__class__.__name__ == "HumanMessage" else "Assistant"
                    history_text += f"{role}: {msg.content}\n"

        # Determine which tool to use
        if use_document is None:
            # Auto-detect: if query mentions document-related terms, use document search
            use_document = self.retriever_tool is not None and (
                "document" in query.lower() or "pdf" in query.lower() or "note" in query.lower() or "lecture" in query.lower()
            )

        source = "document" if use_document else "web"

        # Get response from appropriate tool
        try:
            if use_document and self.retriever_tool:
                tool_result = self.retriever_tool.invoke(query)
                context = f"Document Information:\n{tool_result}\n\n"
            elif self.search_tool is not None:
                tool_result = self.search_tool.invoke(query)
                context = f"Web Search Results:\n{tool_result}\n\n"
            else:
                # No tools available
                context = "No search tools are currently available. Please upload a document or configure web search.\n\n"
                source = "general"
        except Exception as e:
            logger.error(f"Tool invocation failed: {e}")
            context = f"Error retrieving information: {str(e)}\n\n"
            source = "error"

        # Create prompt with context
        full_prompt = f"""You are a helpful AI tutor and research assistant.

Previous conversation:
{history_text}

Current query: {query}

Relevant information:
{context}

Based on the information above, provide a clear, helpful answer. If the information doesn't fully answer the question, say so and provide what you can."""

        # Get LLM response
        try:
            response = llm_service.invoke(full_prompt)
            return {"output": response.content, "source": source}
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            return {"output": f"I apologize, but I encountered an error: {str(e)}", "source": "error"}

    def chat(self, message: str, session_id: str, use_document: bool = None) -> dict:
        """Process a chat message."""
        # Get conversation history
        chat_history = self.memory.get_messages(session_id)

        # Invoke agent
        response = self.agent.invoke({"input": message, "chat_history": chat_history, "use_document": use_document})

        # Save to memory
        self.memory.add_user_message(session_id, message)
        self.memory.add_ai_message(session_id, response.get("output", ""))

        return response

    def clear_session(self, session_id: str):
        """Clear conversation memory for a session."""
        self.memory.clear_session(session_id)

    def get_status(self) -> dict:
        """Get agent status."""
        return {
            "rag_available": rag_service.is_available(),
            "tools_count": len(self.tools),
            "model_name": llm_service.model_name,
        }


# Global agent service instance
agent_service = AgentService()
