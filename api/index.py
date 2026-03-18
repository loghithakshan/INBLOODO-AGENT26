"""
FastAPI entrypoint for Vercel (api/index.py)
Creates and exports the FastAPI app directly for serverless functions
"""
import os
import sys
from pathlib import Path

print("[DEBUG] api/index.py loading...")
sys.stderr.write("[DEBUG] api/index.py loading on stderr\n")
sys.stderr.flush()

# Ensure project root is in path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"[DEBUG] Project root: {project_root}")
print(f"[DEBUG] sys.path updated")

# Create the FastAPI app for Vercel
try:
    print("[DEBUG] Importing src.api_optimized...")
    from src.api_optimized import app
    print("[DEBUG] Successfully imported src.api_optimized.app")
except Exception as e:
    print(f"[ERROR] Failed to import: {str(e)}")
    sys.stderr.write(f"[ERROR] Import failed: {str(e)}\n")
    sys.stderr.flush()
    import traceback
    traceback.print_exc()
    
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

print("[DEBUG] api/index.py finalized, app ready")

# This is the module-level app that Vercel will use
# All requests route through this export

