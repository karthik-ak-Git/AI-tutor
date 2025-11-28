"""
Simple script to run the FastAPI application
"""
import os
import uvicorn
from app.config import settings

if __name__ == "__main__":
    # Use PORT from environment (for Render, Heroku, etc.) or default
    port = int(os.getenv("PORT", settings.PORT))
    # Always use 0.0.0.0 for production (Render requirement)
    host = os.getenv("HOST", "0.0.0.0")
    
    # Disable reload in production (Render doesn't need it)
    # Check if running on Render (has RENDER environment variable)
    is_render = os.getenv("RENDER") is not None
    reload = settings.DEBUG and not is_render
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.LOG_LEVEL.lower()
    )

