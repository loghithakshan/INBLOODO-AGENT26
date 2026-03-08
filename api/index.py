"""Vercel FastAPI entrypoint"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)

# Create necessary directories
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# Import and export the FastAPI app
try:
    from src.api_optimized import app
except ImportError:
    from main import app

# Export app for Vercel
__all__ = ["app"]
