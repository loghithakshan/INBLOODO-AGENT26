import os
import secrets
from fastapi import Header, HTTPException
import logging

logger = logging.getLogger(__name__)

# Generate a secure API key if not provided
DEFAULT_API_KEY = secrets.token_urlsafe(32)
API_KEY = os.getenv("API_KEY", DEFAULT_API_KEY)

# Log the API key for development (remove in production)
if os.getenv("ENVIRONMENT") != "production":
    logger.info(f"API Key: {API_KEY}")

def api_key_required(x_api_key: str | None = Header(None)):
    """
    Validate API key from request headers.
    In development mode, accepts any request with or without API key.
    """
    is_dev = os.getenv("ENVIRONMENT") != "production"
    
    # In development, allow all requests regardless of API key
    if is_dev:
        return x_api_key or API_KEY
    
    # In production, enforce strict API key validation
    if not x_api_key:
        logger.warning("Request missing API key")
        raise HTTPException(
            status_code=401,
            detail="API key required"
        )
    
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key"
        )
    
    return x_api_key