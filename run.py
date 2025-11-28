"""
Simple script to run the FastAPI application
"""
import os
import uvicorn
from app.config import settings

if __name__ == "__main__":
    # Use PORT from environment (for Render, Heroku, etc.) or default
    port = int(os.getenv("PORT", settings.PORT))
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=port,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

