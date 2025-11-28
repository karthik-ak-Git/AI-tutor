# AI Tutor API

A production-ready FastAPI application for AI-powered tutoring with RAG (Retrieval Augmented Generation) and web search capabilities.

## Features

- 📚 **RAG Pipeline**: Answer questions from uploaded PDF documents
- 🌐 **Web Search**: Real-time information via DuckDuckGo
- 🧠 **Memory**: Conversation context awareness
- 🎯 **Smart Routing**: Automatically decides between document search and web search
- 💰 **Cost-Effective**: Uses OpenRouter + free local embeddings
- 🎨 **Frontend**: Built-in chat interface

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file:

```env
OPENROUTER_API_KEY=sk-or-your-key-here
```

### 3. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Frontend interface
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `POST /chat` - Chat with AI tutor
- `POST /document/summary` - Upload and process documents
- `POST /document/query` - Query uploaded documents
- `POST /learn` - Learning modes (explain, quiz, practice)

## Project Structure

```
AI-tutor/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Pydantic schemas
│   ├── services/            # Business logic
│   └── utils/               # Utilities
├── frontend/                # Frontend files
├── tests/                   # Test files
├── requirements.txt         # Dependencies
├── Dockerfile              # Docker config
└── render.yaml             # Render deployment
```

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions.

## Documentation

- [SETUP.md](./SETUP.md) - Detailed setup instructions
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide

## License

MIT
