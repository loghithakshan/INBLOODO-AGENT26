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

def create_app():
    """Create and return the FastAPI application"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Create necessary directories
        Path("data/uploads").mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(parents=True, exist_ok=True)
        
        # Import and return the optimized API
        from src.api_optimized import app as fastapi_app
        logger.info("✅ Successfully loaded FastAPI app from src.api_optimized")
        return fastapi_app
        
    except Exception as e:
        print(f"⚠️  Error loading main API: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback app if main app fails
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
        
        return app

# Create the app at module level for Vercel
app = create_app()

# During development, run with uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n{'='*70}")
    print(f"🚀 INBLOODO AGENT - FastAPI Server")
    print(f"{'='*70}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"📚 Docs:   http://localhost:{port}/docs")
    print(f"🏥 Health: http://localhost:{port}/health")
    print(f"{'='*70}\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
