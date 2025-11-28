"""
FastAPI application entry point
"""
import uuid
import logging
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.models.schemas import (
    ChatRequest, ChatResponse, HealthResponse, ErrorResponse,
    DocumentSummaryRequest, DocumentSummaryResponse, DocumentUploadResponse,
    DocumentQueryRequest, DocumentQueryResponse,
    LearnRequest, LearnResponse
)
from app.services.agent_service import agent_service
from app.services.rag_service import rag_service
from app.services.llm_service import llm_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting AI Tutor API...")
    logger.info(f"RAG Available: {rag_service.is_available()}")
    logger.info(f"Model: {llm_service.model_name}")
    yield
    # Shutdown
    logger.info("Shutting down AI Tutor API...")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
try:
    from pathlib import Path
    frontend_path = Path(__file__).parent.parent / "frontend"
    if frontend_path.exists():
        # Mount static files (CSS, JS) at /static
        app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
        
        @app.get("/")
        async def serve_frontend():
            """Serve the frontend HTML file."""
            return FileResponse(str(frontend_path / "index.html"))
        
        logger.info(f"Frontend files served from: {frontend_path}")
    else:
        logger.warning(f"Frontend directory not found at: {frontend_path}")
        # If frontend not found, provide API root endpoint
        @app.get("/", tags=["Root"])
        async def root():
            """Root endpoint."""
            return {
                "message": "AI Tutor API",
                "version": settings.API_VERSION,
                "docs": "/docs"
            }
except Exception as e:
    logger.warning(f"Frontend files not found: {e}. API will work without frontend.")
    # If frontend not found, provide API root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint."""
        return {
            "message": "AI Tutor API",
            "version": settings.API_VERSION,
            "docs": "/docs"
        }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    status_info = agent_service.get_status()
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        rag_available=status_info["rag_available"],
        tools_count=status_info["tools_count"],
        model_name=status_info["model_name"]
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat endpoint for interacting with the AI tutor.
    
    - **message**: User's question or message
    - **session_id**: Optional session ID for conversation context (auto-generated if not provided)
    - **use_document**: Optional flag to force document search (if available)
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process chat
        result = agent_service.chat(
            message=request.message,
            session_id=session_id,
            use_document=request.use_document
        )
        
        return ChatResponse(
            response=result.get("output", ""),
            session_id=session_id,
            source=result.get("source", "general"),
            metadata={"session_id": session_id}
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


@app.delete("/chat/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    """Clear conversation memory for a specific session."""
    try:
        agent_service.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing session: {str(e)}"
        )


@app.post("/document/upload", response_model=DocumentUploadResponse, tags=["Document"])
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document for RAG-based learning.
    
    - **file**: PDF file to upload
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        document_id = str(uuid.uuid4())
        file_path = upload_dir / f"{document_id}_{file.filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File uploaded: {file_path}")
        
        # Load document into RAG service
        result = rag_service.load_document_from_path(str(file_path))
        
        if result["success"]:
            # Reload agent tools to include new document
            agent_service.reload_tools()
            
            return DocumentUploadResponse(
                message="Document uploaded and processed successfully",
                document_path=str(file_path),
                pages_loaded=result["pages"],
                chunks_created=result["chunks"],
                status="success",
                document_id=document_id
            )
        else:
            # Clean up file if loading failed
            if file_path.exists():
                file_path.unlink()
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process document: {result.get('error', 'Unknown error')}"
            )
    
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )


@app.get("/document/info", tags=["Document"])
async def get_document_info():
    """Get information about the currently loaded document."""
    info = rag_service.get_document_info()
    if not info.get("available"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No document loaded"
        )
    return info


@app.post("/document/summary", response_model=DocumentSummaryResponse, tags=["Document"])
async def process_document_and_summary(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    query: Optional[str] = Form(None),
    source_name: Optional[str] = Form("text_input")
):
    """
    Upload document (PDF or text) and get summary.
    
    - **file**: PDF file to upload (optional)
    - **text**: Text content to process (optional)
    - **query**: Optional query to focus the summary
    - **source_name**: Name for text source
    
    Either file or text must be provided.
    """
    document_id = None
    pages_loaded = None
    chunks_created = None
    
    try:
        # Process file upload if provided
        if file is not None:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PDF files are supported"
                )
            
            # Create uploads directory if it doesn't exist
            upload_dir = Path("uploads")
            upload_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            document_id = str(uuid.uuid4())
            file_path = upload_dir / f"{document_id}_{file.filename}"
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File uploaded: {file_path}")
            
            # Load document into RAG service
            result = rag_service.load_document_from_path(str(file_path))
            
            if not result["success"]:
                if file_path.exists():
                    file_path.unlink()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to process document: {result.get('error', 'Unknown error')}"
                )
            
            pages_loaded = result["pages"]
            chunks_created = result["chunks"]
            
            # Reload agent tools to include new document
            agent_service.reload_tools()
        
        # Process text input if provided
        elif text is not None and text.strip():
            if len(text.strip()) < 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Text content must be at least 10 characters"
                )
            
            document_id = str(uuid.uuid4())
            result = rag_service.load_document_from_text(text, source_name or f"text_{document_id}")
            
            if not result["success"]:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to process text: {result.get('error', 'Unknown error')}"
                )
            
            pages_loaded = result["pages"]
            chunks_created = result["chunks"]
            
            # Reload agent tools
            agent_service.reload_tools()
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either file or text must be provided"
            )
        
        # Generate summary
        if not rag_service.is_available():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Document processed but RAG service is not available"
            )
        
        summary = rag_service.get_document_summary(llm_service.llm, query)
        
        return DocumentSummaryResponse(
            summary=summary,
            status="success",
            pages_loaded=pages_loaded,
            chunks_created=chunks_created,
            document_id=document_id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )


@app.post("/document/query", response_model=DocumentQueryResponse, tags=["Document"])
async def query_document(request: DocumentQueryRequest):
    """
    Query uploaded documents with AI teaching assistance.
    
    The AI will reference the uploaded documents and provide clear,
    educational explanations based on the document content.
    """
    if not rag_service.is_available():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No documents available. Please upload a document first using /document/summary"
        )
    
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Query with teaching mode
        response_text = rag_service.query_with_context(
            query=request.query,
            llm=llm_service.llm,
            teaching_mode=request.teaching_mode
        )
        
        # Get number of relevant chunks (approximate)
        try:
            docs = rag_service._retrieve_documents(request.query)
            relevant_chunks = len(docs)
        except:
            relevant_chunks = None
        
        # Save to memory for context
        agent_service.memory.add_user_message(session_id, request.query)
        agent_service.memory.add_ai_message(session_id, response_text)
        
        return DocumentQueryResponse(
            response=response_text,
            session_id=session_id,
            source="document",
            relevant_chunks=relevant_chunks,
            metadata={
                "teaching_mode": request.teaching_mode,
                "query": request.query
            }
        )
    
    except Exception as e:
        logger.error(f"Error querying document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying document: {str(e)}"
        )


@app.post("/learn", response_model=LearnResponse, tags=["Learn"])
async def learn(request: LearnRequest):
    """
    Learning endpoint with educational features.
    
    Supports different learning modes:
    - **explain**: Get detailed explanations
    - **quiz**: Generate quiz questions
    - **practice**: Practice problems and solutions
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Build learning prompt based on mode
        if request.learning_mode == "quiz":
            prompt = f"""Generate a {request.difficulty} difficulty quiz question about: {request.topic or request.question}

Format:
1. Question
2. Multiple choice options (A, B, C, D)
3. Correct answer
4. Explanation

Make it educational and clear."""
        
        elif request.learning_mode == "practice":
            prompt = f"""Create a {request.difficulty} difficulty practice problem about: {request.topic or request.question}

Include:
1. Problem statement
2. Step-by-step solution
3. Key concepts explained
4. Similar practice suggestions"""
        
        else:  # explain mode
            prompt = f"""Provide a detailed, educational explanation about: {request.topic or request.question}

Make it:
- Clear and easy to understand
- Include examples if helpful
- Break down complex concepts
- Use analogies when appropriate
- Suitable for {request.difficulty} level learners"""
        
        # Use agent to get response
        result = agent_service.chat(
            message=prompt,
            session_id=session_id,
            use_document=True  # Prefer document if available
        )
        
        return LearnResponse(
            response=result.get("output", ""),
            session_id=session_id,
            learning_mode=request.learning_mode or "explain",
            metadata={
                "difficulty": request.difficulty,
                "topic": request.topic or request.question,
                "source": result.get("source", "general")
            }
        )
    
    except Exception as e:
        logger.error(f"Learn error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing learning request: {str(e)}"
        )


@app.post("/learn/ask", response_model=ChatResponse, tags=["Learn"])
async def ask_question(request: ChatRequest):
    """
    Ask a question about the uploaded document or general knowledge.
    This is an alias for /chat with document preference.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process chat with document preference
        result = agent_service.chat(
            message=request.message,
            session_id=session_id,
            use_document=request.use_document if request.use_document is not None else True
        )
        
        return ChatResponse(
            response=result.get("output", ""),
            session_id=session_id,
            source=result.get("source", "general"),
            metadata={
                "session_id": session_id,
                "learning_mode": "ask"
            }
        )
    
    except Exception as e:
        logger.error(f"Ask error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return ErrorResponse(
        error="Internal server error",
        detail=str(exc),
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn
    import os
    # Use PORT from environment (for Render, Heroku, etc.) or default
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=port,
        reload=settings.DEBUG
    )

