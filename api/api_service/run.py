#!/usr/bin/env python3
"""
Runner script for the NLP Data Anonymizer API Service.
"""
import uvicorn
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import settings from the config module
from api_service.config import settings

def main():
    """Run the FastAPI application using Uvicorn."""
    print(f"Starting NLP Data Anonymizer API Service on {settings.HOST}:{settings.PORT}")
    print(f"Default LLM provider: {settings.DEFAULT_PROVIDER}")
    print(f"Debug mode: {'enabled' if settings.DEBUG else 'disabled'}")
    print(f"\nAccess the API documentation at: http://127.0.0.1:{settings.PORT}/docs")
    
    uvicorn.run(
        "api_service.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    main() 