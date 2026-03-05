# Blood Report AI - Deployment Guide

## Quick Start Deployment

### Option 1: Railway (⭐ RECOMMENDED)
Railway is the best choice for this Python application - no memory limitations.

**Steps:**
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select: `loghithakshan/INBLOODO-AGENT26`
5. Railway automatically detects the Dockerfile
6. Add environment variables in Project Settings:
   - `GEMINI_API_KEY=your_key`
   - `OPENAI_API_KEY=your_key`
   - `ANTHROPIC_API_KEY=your_key`
   - `GROK_API_KEY=your_key`
7. Click **Deploy**
8. Your app will be live in 2-5 minutes!

**Estimated Cost:** $5-10/month on Railway starter plan

---

### Option 2: Render
Another great alternative with better Python support than Vercel.

**Steps:**
1. Go to https://render.com
2. Sign up with GitHub
3. Click **"Create"** → **"Web Service"**
4. Connect GitHub repository: `loghithakshan/INBLOODO-AGENT26`
5. Configure:
   - **Environment:** Docker
   - **Region:** Choose closest to users
   - **Plan:** Starter ($7/month) or Standard ($25/month)
6. Add environment variables
7. Click **"Create Web Service"**

---

### Option 3: Heroku (Alternative)
If you prefer Heroku, see heroku.yml configuration (coming soon)

---

## Deployment Files Included

✅ **Dockerfile** - Container configuration for Railway/Render
✅ **railway.json** - Railway-specific settings
✅ **requirements.txt** - All Python dependencies
✅ **.gitignore** - Excludes unnecessary files
✅ **app.py** - FastAPI entrypoint for serverless
✅ **vercel.json** - Vercel configuration (if you upgrade to Pro)

---

## Environment Variables Needed

```
GEMINI_API_KEY=your_google_gemini_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
GROK_API_KEY=your_grok_api_key
HOST=0.0.0.0
PORT=8000
DEBUG=false
DATABASE_URL=sqlite:///./blood_reports.db
```

---

## Post-Deployment

Once deployed:
1. Visit your deployment URL
2. Try uploading a blood report PDF
3. Test multi-AI analysis
4. Check `/docs` for API documentation

---

## Comparison

| Platform | Memory | Cost | Setup | Python Support |
|----------|--------|------|-------|-----------------|
| **Railway** ⭐ | 16GB+ | $5-10/mo | Easy | Excellent |
| **Render** | 1GB+ | $7+/mo | Easy | Great |
| Vercel Hobby | 2GB | Free | Simple | Limited |
| Vercel Pro | Unlimited | $20/mo | Simple | Good |
| Heroku | 512MB | (Shutdown) | Easy | Good |

**Recommendation:** Use **Railway** for best value and reliability.

---

## Troubleshooting

**If deployment fails:**
1. Check build logs in dashboard
2. Verify all dependencies in requirements.txt
3. Check that API keys are set as environment variables
4. Ensure .gitignore excludes large folders

**If PDF processing fails:**
1. Make sure tesseract-ocr is installed (in Dockerfile)
2. Check EasyOCR models are downloading (takes first run)
3. Increase memory allocation if available

---

## Support URLs

- Railway: https://railway.app/docs
- Render: https://render.com/docs
- GitHub Repo: https://github.com/loghithakshan/INBLOODO-AGENT26
