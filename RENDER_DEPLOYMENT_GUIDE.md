# Deploy to Render (Alternative to Railway)

## Why Render?
- ✅ Similar to Railway but with different infrastructure
- ✅ Free tier available ($0-10/month)
- ✅ GitHub integration (auto-deploy on push)
- ✅ 99.9% uptime SLA
- ✅ HTTPS/SSL included
- ✅ Auto-scaling
- ✅ Environment variables built-in

---

## Step 1: Go to Render
1. Visit: **https://render.com**
2. Click: **"Sign up"**
3. Choose: **"Continue with GitHub"**
4. Authorize Render to access your GitHub account

---

## Step 2: Create New Web Service
1. Dashboard → Click: **"New +"** button (top right)
2. Select: **"Web Service"**
3. Select Repository: **"loghithakshan/INBLOODO-AGENT26"**
4. Click: **"Connect"**

---

## Step 3: Configure Service

### Basic Settings:
- **Name:** `blood-report-ai` (or your preferred name)
- **Environment:** `Docker` (auto-detected from Dockerfile)
- **Region:** `Oregon` (closest to you, or pick your region)
- **Branch:** `main`

### Auto-Deploy:
- ✅ Check: **"Auto-deploy"** (deploys on every push to main)

---

## Step 4: Add Environment Variables

Click: **"Environment"** in left sidebar

Add these variables (click **"Add Environment Variable"** for each):

```
GEMINI_API_KEY=your_actual_key_here
OPENAI_API_KEY=your_actual_key_here
ANTHROPIC_API_KEY=your_actual_key_here
GROK_API_KEY=your_actual_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

**⚠️ Replace with YOUR ACTUAL API KEYS from:**
- Google AI Studio: https://aistudio.google.com/app/apikey
- OpenAI: https://platform.openai.com/account/api-keys
- Anthropic: https://console.anthropic.com/account/keys
- Grok: https://console.x.ai/

---

## Step 5: Deploy!

1. Click: **"Create Web Service"** button (bottom right)
2. Wait: 3-5 minutes for build and deployment
3. Check: Build logs display in real-time

---

## Step 6: Access Your Live App

Once deployment completes (Status = **"Live"**):

1. Find your URL in the dashboard (top of service page)
   - Format: `https://blood-report-ai-xxxxx.onrender.com`

2. Access your app:
   - **Main App:** `https://your-url.onrender.com/`
   - **API Docs:** `https://your-url.onrender.com/docs`
   - **Health Check:** `https://your-url.onrender.com/health`

---

## Features Render Provides

✅ **24/7 Uptime**
- Auto-restarts on crashes
- Health checks enabled
- Monitoring dashboard

✅ **Auto-Deploy**
- Push to GitHub main branch
- Automatically redeploys
- No manual deployment needed

✅ **Logs & Monitoring**
- Real-time logs
- Instance metrics
- Error tracking

✅ **Custom Domain** (optional)
- Add your own domain
- Auto HTTPS certificates
- DNS configuration guide

---

## Troubleshooting

### Status Shows "Deploy Failed"
1. Check Build Logs for errors
2. Verify environment variables are set correctly
3. Check Dockerfile is valid
4. Try rebuilding: **Menu → Redeploy**

### Port/Connection Issues
- Render automatically detects port from `PORT` env var
- Default: 8000 (already configured)

### App Crashes on Startup
1. Check logs for Python errors
2. Verify all API keys are correct
3. Check requirements.txt for missing packages

---

## Render vs Railway Comparison

| Feature | Render | Railway |
|---------|--------|---------|
| **Uptime** | 99.9% | 99.9% |
| **Cost** | Free tier + paid | $5/month min |
| **Cold Starts** | None | None |
| **Auto-deploy** | ✅ Yes | ✅ Yes |
| **GitHub Integration** | ✅ Excellent | ✅ Excellent |
| **Infrastructure** | US-based | Global |
| **Support** | Community | Community |

---

## Cost Breakdown

- **Free Tier:** Limited, web service spins down after 15min inactivity
- **Pay-as-you-go:** ~$0.10 per hour running (~$72/month 24/7)
- **Render Plus:** $19/month (includes always-on)

For 24/7 uptime, use **Render Plus** plan.

---

## Next Steps After Deployment

1. ✅ Test your live URL
2. ✅ Upload a blood report image
3. ✅ Test API at `/docs`
4. ✅ Check logs in dashboard
5. ✅ Set up custom domain (optional)
6. ✅ Share your public URL!

---

## Dashboard Navigation

**Render Dashboard → Your Service:**
- **Logs:** Real-time application logs
- **Metrics:** CPU, memory, network usage
- **Environment:** Manage environment variables
- **Settings:** Change region, branch, build settings
- **Events:** View deployment history

---

## If You Want to Switch Back to Railway

Both work identically! You can:
- Keep Render live
- Deploy to Railway simultaneously (same GitHub repo)
- Switch between them anytime
- Both auto-deploy from same main branch

---

## Questions?

- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **GitHub:** https://github.com/loghithakshan/INBLOODO-AGENT26

---

**Your Blood Report AI is ready to deploy on Render!** 🚀
