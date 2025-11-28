"""
Pydantic schemas for request/response validation
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""

    message: str = Field(..., description="User's question or message", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")
    use_document: Optional[bool] = Field(None, description="Force use document search (if available)")

    class Config:
        json_schema_extra = {
            "example": {"message": "What is the capital of France?", "session_id": "user-123", "use_document": False}
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    response: str = Field(..., description="AI tutor's response")
    session_id: str = Field(..., description="Session ID")
    source: str = Field(..., description="Source of information: 'document', 'web', or 'general'")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Paris is the capital of France.",
                "session_id": "user-123",
                "source": "web",
                "metadata": {"tokens_used": 150},
            }
        }


class DocumentUploadResponse(BaseModel):
    """Response model for document upload"""

    message: str
    document_path: str
    pages_loaded: int
    chunks_created: int
    status: str
    document_id: Optional[str] = None


class DocumentSummaryRequest(BaseModel):
    """Request model for document summary with upload and text"""

    file: Optional[str] = Field(None, description="Base64 encoded PDF file (optional)")
    text: Optional[str] = Field(None, description="Text content to process (optional)")
    query: Optional[str] = Field(None, description="Optional query for summary focus")
    source_name: Optional[str] = Field("text_input", description="Name for text source")


class DocumentSummaryResponse(BaseModel):
    """Response model for document summary"""

    summary: str
    status: str
    pages_loaded: Optional[int] = None
    chunks_created: Optional[int] = None
    document_id: Optional[str] = None


class DocumentQueryRequest(BaseModel):
    """Request model for querying documents"""

    query: str = Field(..., description="Question or query about the document", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for context")
    teaching_mode: Optional[bool] = Field(True, description="Enable teaching mode for clear explanations")


class DocumentQueryResponse(BaseModel):
    """Response model for document query"""

    response: str = Field(..., description="AI tutor's response with document context")
    session_id: str
    source: str = "document"
    relevant_chunks: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class LearnRequest(BaseModel):
    """Request model for learning features"""

    topic: Optional[str] = Field(None, description="Topic to learn about")
    question: Optional[str] = Field(None, description="Question to ask")
    session_id: Optional[str] = Field(None, description="Session ID for context")
    difficulty: Optional[str] = Field("medium", description="Difficulty level: easy, medium, hard")
    learning_mode: Optional[str] = Field("explain", description="Learning mode: explain, quiz, practice")


class LearnResponse(BaseModel):
    """Response model for learning features"""

    response: str
    session_id: str
    learning_mode: str
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Response model for health check"""

    status: str
    version: str
    rag_available: bool
    tools_count: int
    model_name: str


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str
    detail: Optional[str] = None
    status_code: int
