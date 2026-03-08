"""Vercel FastAPI entrypoint - Root level app.py equivalent"""
import sys
import os
from pathlib import Path

try:
    # Add project root to Python path
    root_path = Path(__file__).parent.parent
    if str(root_path) not in sys.path:
        sys.path.insert(0, str(root_path))
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Set up logging
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Create necessary directories
    Path("data/uploads").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    
    # Import the FastAPI application
    from src.api_optimized import app
    logger.info("✅ FastAPI app loaded from src.api_optimized")
    
except Exception as e:
    print(f"❌ Error loading FastAPI app: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback: create a minimal FastAPI app
    from fastapi import FastAPI
    app = FastAPI(
        title="INBLOODO AGENT",
        version="2.0.0",
        description="Blood Report AI - Fallback Mode"
    )
    
    @app.get("/")
    def read_root():
        return {"message": "FastAPI app loaded in fallback mode", "error": str(e)}
    
    @app.get("/health")
    def health_check():
        return {"status": "running", "mode": "fallback"}

# Ensure app is exported for Vercel
__all__ = ["app"]
