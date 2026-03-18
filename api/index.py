"""
Vercel Python Serverless Function
App variable must be available at module level for Vercel
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import app from root app.py
from app import app
