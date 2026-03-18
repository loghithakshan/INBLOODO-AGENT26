"""
FastAPI entrypoint for Vercel (api/index.py)
Creates and exports the FastAPI app directly for serverless functions
"""
import os
import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Create the FastAPI app for Vercel
try:
    from src.api_optimized import app
except Exception as e:
    # Fallback if main app fails
    from fastapi import FastAPI
    app = FastAPI(
        title="INBLOODO AGENT",
        version="2.0.0",
    )
    
    @app.get("/")
    def read_root():
        return {"error": f"Failed to load app: {str(e)}", "status": "fallback"}
    
    @app.get("/health")
    def health():
        return {"status": "error", "message": str(e)}

# This is the module-level app that Vercel will use
# All requests route through this export

