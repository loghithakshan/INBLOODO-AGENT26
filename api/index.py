"""
Vercel Serverless Function Entry Point
This file serves as the entry point for Vercel deployments
"""
from app import app

# Export the app for Vercel
__all__ = ['app']
