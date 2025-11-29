#!/bin/bash
# Start script for Render deployment
# This ensures the app binds to 0.0.0.0 and uses $PORT

python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}


