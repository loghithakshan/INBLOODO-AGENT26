"""
FastAPI application entrypoint - used by Vercel and other deployment platforms
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup path and environment
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create required directories
Path("data/uploads").mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(parents=True, exist_ok=True)

# Import and configure the FastAPI application
try:
    from src.api_optimized import app
    logger.info("FastAPI application loaded successfully from src.api_optimized")
except ImportError as e:
    logger.error(f"Failed to load FastAPI application: {e}")
    raise

# Ensure app is available at module level
__all__ = ["app"]
