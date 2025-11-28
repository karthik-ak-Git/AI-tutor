"""
RAG (Retrieval Augmented Generation) service for document processing
"""

from pathlib import Path
from typing import Optional, List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.tools import Tool
from app.config import settings
from app.services.embeddings_service import embeddings_service
import logging
import uuid

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG operations with persistent storage."""

    def __init__(self):
        """Initialize RAG service."""
        self.retriever = None
        self.vectorstore = None
        self.current_document_path = None
        self.document_metadata = {}
        self.persist_directory = Path("chroma_db")
        self.persist_directory.mkdir(exist_ok=True)
        self._load_or_create_vectorstore()

    def _load_or_create_vectorstore(self):
        """Load existing vectorstore or create new one."""
        try:
            # Try to load existing vectorstore
            if (self.persist_directory / "chroma.sqlite3").exists():
                logger.info("Loading existing vectorstore from database")
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory), embedding_function=embeddings_service.get_embeddings()
                )
                self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": settings.RETRIEVER_K})
                logger.info("Vectorstore loaded successfully")
            else:
                # Load initial document if specified
                self._load_document(settings.PDF_PATH)
        except Exception as e:
            logger.warning(f"Could not load existing vectorstore: {e}")
            self._load_document(settings.PDF_PATH)

    def _load_document(self, pdf_path: Optional[str] = None):
        """Load PDF document and add to vector store."""
        if pdf_path is None:
            pdf_path = settings.PDF_PATH

        if not pdf_path or not Path(pdf_path).exists():
            logger.warning(f"PDF not found: {pdf_path}. RAG will not be available.")
            return

        try:
            logger.info(f"Loading PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} pages")

            self._process_and_store_documents(docs, pdf_path)

        except Exception as e:
            logger.error(f"Failed to load document: {e}")

    def _process_and_store_documents(self, docs: List[Document], source: str):
        """Process documents and store in vector database."""
        try:
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
                separators=["\n\n", "\n", " ", ""],
            )

            splits = text_splitter.split_documents(docs)
            logger.info(f"Split into {len(splits)} chunks")

            # Add metadata to chunks
            for split in splits:
                if "source" not in split.metadata:
                    split.metadata["source"] = source

            # Create or add to vector store
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=splits,
                    embedding=embeddings_service.get_embeddings(),
                    persist_directory=str(self.persist_directory),
                )
            else:
                # Add to existing vectorstore
                self.vectorstore.add_documents(splits)
                self.vectorstore.persist()

            # Create/update retriever
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": settings.RETRIEVER_K})

            self.current_document_path = source
            self.document_metadata = {"pages": len(docs), "chunks": len(splits), "path": source}

            logger.info(f"Documents stored in database with {len(splits)} chunks")

        except Exception as e:
            logger.error(f"Failed to process documents: {e}")
            raise

    def load_document_from_path(self, pdf_path: str) -> dict:
        """Load a document from a file path and return metadata."""
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} pages from {pdf_path}")

            self._process_and_store_documents(docs, pdf_path)

            if self.is_available():
                return {
                    "success": True,
                    "pages": self.document_metadata.get("pages", 0),
                    "chunks": self.document_metadata.get("chunks", 0),
                    "path": pdf_path,
                }
            else:
                return {"success": False, "error": "Failed to load document"}
        except Exception as e:
            logger.error(f"Error loading document: {e}")
            return {"success": False, "error": str(e)}

    def load_document_from_text(self, text: str, source_name: str = "text_input") -> dict:
        """Load document from text input and store in database."""
        try:
            # Create document from text
            doc = Document(page_content=text, metadata={"source": source_name, "type": "text_input"})

            self._process_and_store_documents([doc], source_name)

            if self.is_available():
                return {"success": True, "pages": 1, "chunks": self.document_metadata.get("chunks", 0), "path": source_name}
            else:
                return {"success": False, "error": "Failed to process text"}
        except Exception as e:
            logger.error(f"Error loading text: {e}")
            return {"success": False, "error": str(e)}

    def _retrieve_documents(self, query: str) -> List[Document]:
        """Retrieve documents using compatible method."""
        try:
            # Try invoke() first (newer LangChain versions)
            if hasattr(self.retriever, "invoke"):
                result = self.retriever.invoke(query)
                # invoke() returns a list directly
                if isinstance(result, list):
                    return result
                return [result] if result else []
            # Fallback to get_relevant_documents() (older versions)
            elif hasattr(self.retriever, "get_relevant_documents"):
                return self.retriever.get_relevant_documents(query)
            else:
                # Last resort: try calling directly
                result = self.retriever(query)
                return list(result) if result else []
        except Exception as e:
            logger.error(f"Retrieval method error: {e}")
            # Try alternative methods
            try:
                if hasattr(self.retriever, "get_relevant_documents"):
                    return self.retriever.get_relevant_documents(query)
            except Exception:
                pass
            raise

    def get_retriever_tool(self) -> Optional[Tool]:
        """Get the retriever tool if available."""
        if self.retriever is None:
            return None

        def search_document_func(query: str) -> str:
            """Search the uploaded PDF document for relevant information."""
            try:
                docs = self._retrieve_documents(query)
                if not docs:
                    return "No relevant information found in the document."

                # Combine all retrieved chunks
                result = "\n\n".join([f"Excerpt {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
                return result
            except Exception as e:
                logger.error(f"Document search failed: {e}")
                return f"Error searching document: {str(e)}"

        return Tool(
            name="search_document",
            func=search_document_func,
            description="Searches and returns relevant excerpts from the uploaded PDF document. "
            "Use this tool when the user asks questions about the document, specific concepts "
            "mentioned in the document, or requests explanations based on the document content.",
        )

    def is_available(self) -> bool:
        """Check if RAG is available."""
        return self.retriever is not None

    def get_document_info(self) -> dict:
        """Get information about the current document."""
        if not self.is_available():
            return {"available": False}
        return {"available": True, "path": self.current_document_path, **self.document_metadata}

    def get_document_summary(self, llm: any, query: Optional[str] = None) -> str:  # type: ignore
        """Get a summary of the uploaded document using RAG."""
        if not self.is_available():
            return "No document loaded."

        try:
            # Use custom query or default
            search_query = query or "summary of main topics and key concepts"

            # Retrieve relevant chunks using compatible method
            docs = self._retrieve_documents(search_query)

            # Use LLM to generate summary
            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = f"""Based on the following document excerpts, provide a concise summary 
            of the main topics and key concepts:
            
            {context}
            
            Summary:"""

            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Failed to generate document summary: {e}")
            return f"Error generating summary: {str(e)}"

    def query_with_context(self, query: str, llm: any, teaching_mode: bool = True) -> str:  # type: ignore
        """Query documents with context and provide teaching response."""
        if not self.is_available():
            return "No documents available. Please upload a document first."

        try:
            # Retrieve relevant chunks using compatible method
            docs = self._retrieve_documents(query)

            if not docs:
                return "I couldn't find relevant information in the uploaded documents. Please try rephrasing your question or upload relevant documents."

            # Combine context
            context = "\n\n".join(
                [
                    f"Excerpt {i+1} (from {doc.metadata.get('source', 'document')}):\n{doc.page_content}"
                    for i, doc in enumerate(docs)
                ]
            )

            # Create teaching prompt
            if teaching_mode:
                prompt = f"""You are an AI tutor helping a student learn. The student asked: "{query}"

Relevant information from the documents:
{context}

Provide a clear, educational response that:
1. Directly answers the question using information from the documents
2. Explains concepts clearly and step-by-step
3. Uses examples from the documents when helpful
4. Encourages learning and understanding
5. Cites which parts of the document you're referencing

Make your response educational, clear, and helpful for learning."""
            else:
                prompt = f"""Based on the following document excerpts, answer this question: {query}

Document excerpts:
{context}

Answer:"""

            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Query with context failed: {e}")
            return f"Error processing query: {str(e)}"


# Global RAG service instance
rag_service = RAGService()
