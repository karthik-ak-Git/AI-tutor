# AI Tutor & Research Agent

A complete Jupyter Notebook implementation of an intelligent AI tutor that combines RAG (Retrieval Augmented Generation) with real-time web search capabilities.

## Features

- 📚 **RAG Pipeline**: Answer questions from uploaded PDF documents
- 🌐 **Web Search**: Real-time information via DuckDuckGo
- 🧠 **Memory**: Conversation context awareness
- 🎯 **Smart Routing**: Automatically decides between document search and web search
- 💰 **Cost-Effective**: Uses OpenRouter + free local embeddings

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

Run Cell 1 in the notebook, or install manually:

```bash
pip install langchain langchain-openai langchain-community faiss-cpu pypdf sentence-transformers duckduckgo-search python-dotenv
```

### 3. Setup API Keys

1. Get your OpenRouter API key from [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Create a `.env` file in the project directory:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### 4. Prepare Your PDF

Place your PDF file (e.g., `lecture_notes.pdf`) in the same directory as the notebook, or update the `PDF_PATH` variable in Cell 4.

### 5. Run the Notebook

Open `ai_tutor_research_agent.ipynb` in Jupyter and run cells sequentially.

## Usage

### Interactive Mode

Run Cell 7 to start an interactive chat session:

- Ask questions about your document: "What are the main topics in the lecture notes?"
- Search the web: "What is the latest news about AI?"
- Follow-up questions: The agent remembers context

Type `quit`, `exit`, or `bye` to end the session.

### Quick Test Mode

Run Cell 8 for quick single-query tests without the interactive loop.

## Architecture

```
User Query
    ↓
Agent (with Memory)
    ↓
Router Decision
    ├─→ Document Question? → RAG Retriever → Vector Store (FAISS)
    └─→ General Question? → DuckDuckGo Search
    ↓
LLM (OpenRouter: gpt-4o-mini)
    ↓
Response with Sources
```

## Tech Stack

- **LangChain**: Orchestration framework
- **OpenRouter**: LLM API (gpt-4o-mini)
- **HuggingFace**: Local embeddings (sentence-transformers/all-MiniLM-L6-v2)
- **ChromaDB**: Vector database (in-memory)
- **DuckDuckGo**: Free web search
- **PyPDF**: PDF text extraction

## Cost Estimation

- **LLM (OpenRouter)**: ~$0.01-0.10 per 1000 queries
- **Embeddings**: Free (local HuggingFace model)
- **Web Search**: Free (DuckDuckGo)
- **Total**: Very cost-effective for educational use

## Troubleshooting

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt` (if you create one)

### API Errors
- Verify OpenRouter API key is correct
- Check your OpenRouter account has credits
- Ensure internet connection is active

### PDF Not Found
- Update `PDF_PATH` variable in Cell 4
- Ensure PDF file is in the correct directory

### Memory Issues
- Reduce `chunk_size` in Cell 4 (e.g., from 1000 to 500)
- Use a smaller PDF file

## File Structure

```
AI-tutor/
├── ai_tutor_research_agent.ipynb  # Main notebook
├── .env                            # API keys (not in git)
├── .env.example                    # Template for .env
├── README.md                       # This file
└── lecture_notes.pdf              # Your PDF (optional)
```

## Notes

- The notebook is designed to run cell-by-cell
- Each cell includes comments explaining the purpose
- The agent automatically routes queries to the appropriate tool
- Source citations are included when using RAG
- Memory persists throughout the session

## License

This is a prototype/educational project. Feel free to modify and use as needed.

