
# Blood Report AI - Deployment Quick Reference

## Current Status
- **Repository**: https://github.com/loghithakshan/INBLOODO-AGENT26
- **Branch**: main
- **Size**: ~233 MB (under 2GB limit)
- **Files**: 380+ files configured

## Deployment URLs
- GitHub: https://github.com/loghithakshan/INBLOODO-AGENT26
- Railway: https://railway.app/dashboard
- API Docs: /docs (after deployment)
- Health: /health (after deployment)

## Environment Variables Needed
```
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
GROK_API_KEY=your_key
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## Key Files
- `Dockerfile` - Docker configuration
- `railway.json` - Railway settings
- `main.py` - Application entry
- `requirements.txt` - Dependencies
- `app.py` - FastAPI app export

## Troubleshooting
- Port in use? Try: set PORT=8001
- Module not found? Run: pip install -r requirements.txt
- Can't deploy? Check .gitignore excludes venv/

## Support Resources
- Railway Docs: https://railway.app/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- GitHub Repo: https://github.com/loghithakshan/INBLOODO-AGENT26
