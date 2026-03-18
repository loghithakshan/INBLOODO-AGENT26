"""
FastAPI Application - Root Level Entrypoint
Vercel will find this app.py and use it as the main application
"""
import os
import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Setup environment and logging
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create necessary directories
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# Import and export the app directly from src.api_optimized
try:
    from src.api_optimized import app
    logger.info("[OK] Successfully loaded FastAPI app from src.api_optimized")
except Exception as e:
    logger.error(f"[ERROR] Failed to import src.api_optimized: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback app if import fails
    from fastapi import FastAPI
    app = FastAPI(
        title="INBLOODO AGENT",
        version="2.0.0",
        description="Blood Report AI Analysis System"
    )
    
    @app.get("/")
    def read_root():
        return {"status": "running", "mode": "fallback", "error": str(e)}
    
    @app.get("/health")
    def health_check():
        return {"status": "operational", "version": "2.0.0"}

# During development, run with uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print("\n" + "="*70)
    print("[STARTUP] INBLOODO AGENT - FastAPI Server")
    print("="*70)
    print(f"[INFO] Server: http://localhost:{port}")
    print(f"[INFO] Docs:   http://localhost:{port}/docs")
    print(f"[INFO] Health: http://localhost:{port}/health")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
