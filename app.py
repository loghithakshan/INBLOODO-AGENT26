"""
FastAPI Application - Root Level Entrypoint
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Create necessary directories
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# Import FastAPI app - THIS MUST BE AT MODULE LEVEL FOR VERCEL
from src.api_optimized import app

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
