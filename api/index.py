"""
Vercel Serverless Function Handler for FastAPI
This is the standard Vercel Python entrypoint for FastAPI apps
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize app  
from app import app

# Export for Vercel serverless
__all__ = ['app']
