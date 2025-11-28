# Setup Instructions

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Environment File**
   Create a `.env` file in the project root with:
   ```env
   OPENROUTER_API_KEY=sk-or-your-key-here
   OPENROUTER_MODEL=openai/gpt-4.1-nano
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_TEMPERATURE=0.5
   OPENROUTER_TIMEOUT=30
   
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   EMBEDDING_DEVICE=cpu
   
   PDF_PATH=DSA Handwritten Notes.pdf
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   RETRIEVER_K=4
   
   SEARCH_MAX_RESULTS=10
   
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   LOG_LEVEL=INFO
   ```

3. **Run the API**
   ```bash
   python run.py
   # Or
   uvicorn app.main:app --reload
   ```

4. **Access API Docs**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Docker Setup

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html
```


