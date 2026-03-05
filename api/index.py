"""
Vercel serverless function entrypoint for FastAPI
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Create required directories
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# Import the FastAPI app
from src.api_optimized import app

# Export the app for Vercel
_app = app
