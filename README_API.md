# AI Tutor API

Production-ready FastAPI backend for the AI Tutor & Research Agent.

## Features

- 🤖 **AI Tutor Agent**: Intelligent routing between document search and web search
- 📚 **RAG Pipeline**: Document-based question answering
- 🌐 **Web Search**: Real-time information via DuckDuckGo
- 💬 **Conversation Memory**: Session-based conversation context
- 🚀 **FastAPI**: High-performance async API
- 🐳 **Docker Support**: Containerized deployment
- 🔄 **CI/CD**: Automated testing and deployment pipeline

## Project Structure

```
AI-tutor/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── agent_service.py  # Agent orchestration
│       ├── llm_service.py    # LLM integration
│       ├── rag_service.py    # RAG pipeline
│       ├── search_service.py # Web search
│       ├── embeddings_service.py # Embeddings
│       └── memory.py         # Conversation memory
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image
├── docker-compose.yml       # Docker Compose setup
└── README_API.md           # This file
```

## Setup

### 1. Clone and Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
OPENROUTER_API_KEY=sk-or-your-key-here
```

### 3. Place Your PDF (Optional)

Place your PDF file in the project root or update `PDF_PATH` in `.env`:

```bash
# Example
PDF_PATH=DSA Handwritten Notes.pdf
```

## Running the API

### Development Mode

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use Python
python -m app.main
```

### Production Mode

```bash
# Using Docker
docker-compose up -d

# Or build and run manually
docker build -t ai-tutor .
docker run -p 8000:8000 --env-file .env ai-tutor
```

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "rag_available": true,
  "tools_count": 2,
  "model_name": "openai/gpt-4.1-nano"
}
```

### Chat

```bash
POST /chat
Content-Type: application/json

{
  "message": "What is the capital of France?",
  "session_id": "optional-session-id",
  "use_document": false
}
```

Response:
```json
{
  "response": "Paris is the capital of France...",
  "session_id": "uuid-here",
  "source": "web",
  "metadata": {
    "session_id": "uuid-here"
  }
}
```

### Upload Document

```bash
POST /document/upload
Content-Type: multipart/form-data

file: [PDF file]
```

Response:
```json
{
  "message": "Document uploaded and processed successfully",
  "document_path": "uploads/uuid_filename.pdf",
  "pages_loaded": 50,
  "chunks_created": 37,
  "status": "success",
  "document_id": "uuid-here"
}
```

### Ask Question (Document-focused)

```bash
POST /learn/ask
Content-Type: application/json

{
  "message": "What are the main topics in the document?",
  "session_id": "optional-session-id",
  "use_document": true
}
```

### Learn Mode

```bash
POST /learn
Content-Type: application/json

{
  "topic": "Data Structures",
  "session_id": "optional-session-id",
  "difficulty": "medium",
  "learning_mode": "explain"
}
```

Learning modes:
- `explain`: Get detailed explanations
- `quiz`: Generate quiz questions
- `practice`: Practice problems and solutions

### Document Info

```bash
GET /document/info
```

### Document Summary

```bash
GET /document/summary
```

### Clear Session

```bash
DELETE /chat/{session_id}
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Tests**: Runs linting, type checking, and tests
2. **Builds**: Creates Docker image
3. **Validates**: Tests Docker container

To use:
1. Push code to GitHub
2. Workflow runs automatically on push/PR
3. Check Actions tab for status

## Configuration

All configuration is managed through environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `OPENROUTER_MODEL` | LLM model name | `openai/gpt-4.1-nano` |
| `PDF_PATH` | Path to PDF document | Optional |
| `CHUNK_SIZE` | Document chunk size | `1000` |
| `RETRIEVER_K` | Number of chunks to retrieve | `4` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

### Code Structure

- **`app/main.py`**: FastAPI application and routes
- **`app/services/`**: Business logic services
- **`app/models/`**: Pydantic schemas for validation
- **`app/config.py`**: Configuration management

### Adding New Features

1. Add service in `app/services/`
2. Create schema in `app/models/schemas.py`
3. Add endpoint in `app/main.py`
4. Update tests (if applicable)

## Deployment

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Considerations

1. **Environment Variables**: Use secure secret management
2. **CORS**: Configure `allow_origins` in `main.py`
3. **Rate Limiting**: Add rate limiting middleware
4. **Monitoring**: Add APM/monitoring tools
5. **Logging**: Configure centralized logging
6. **SSL/TLS**: Use reverse proxy (nginx) with SSL

## Troubleshooting

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### PDF Not Loading

- Check `PDF_PATH` in `.env`
- Ensure PDF file exists at specified path
- Check file permissions

### API Key Issues

- Verify `OPENROUTER_API_KEY` in `.env`
- Check API key has credits
- Ensure internet connection

## License

This is a prototype/educational project. Feel free to modify and use as needed.

