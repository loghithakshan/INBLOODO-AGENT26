# Deploy to Google Cloud Run (Alternative to Railway)

## Why Google Cloud Run?

✅ **Best for containers**
- Free tier: 2 million requests/month
- Generous free CPU quota
- Pay only for what you use ($0.40/million requests)
- No cost for idle time (unlike App Engine)

✅ **Enterprise Features**
- Auto-scaling (0 to thousands of instances)
- Built-in security & identity
- Integrated monitoring (Cloud Logging, Cloud Trace)
- Global load balancing
- Custom domains support

✅ **Easy GitHub Integration**
- Deploy directly from GitHub
- Auto-deploy on push (Cloud Build)
- No Dockerfile needed (optional)

---

## Quick Start (5 minutes)

### Step 1: Create Google Cloud Account
1. Go: **https://cloud.google.com/run**
2. Click: **"Start for free"**
3. Create account with Google
4. Verify payment method (no charge for free tier)

### Step 2: Enable Cloud Run API
1. Go to: **https://console.cloud.google.com**
2. Search: **"Cloud Run"** in search box
3. Click: **"Enable API"**
4. Wait for API to enable (30 seconds)

### Step 3: Deploy from GitHub

#### Option A: Using Cloud Console (Easiest)

1. Go: **https://console.cloud.google.com/run**
2. Click: **"Create Service"**
3. Select: **"Deploy one revision from source code"**
4. Choose: **"GitHub"**
5. Click: **"Set up with Cloud Build"**
6. Connect GitHub account
7. Select Repository: **`loghithakshan/INBLOODO-AGENT26`**
8. Branch: **`main`**
9. Build Type: **`Dockerfile`** (auto-detected)

#### Configuration:
- **Service Name:** `blood-report-ai`
- **Region:** `us-central1` (or nearest to you)
- **Memory:** `512 MB` (sufficient for your app)
- **CPU:** `1` (auto-scaling enabled)

#### Step 4: Set Environment Variables

In "Runtime settings":

```
GEMINI_API_KEY=your_actual_key
OPENAI_API_KEY=your_actual_key
ANTHROPIC_API_KEY=your_actual_key
GROK_API_KEY=your_actual_key
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

#### Step 5: Deploy!

Click: **"Create"** button
- Build starts automatically
- Deployment takes 2-5 minutes
- Status shows in real-time

---

## Access Your Live App

Once deployed (Status = **"Ready"**):

Your URL appears at top of service page:
```
https://blood-report-ai-xxxxx-uc.a.run.app
```

Access:
- **Main:** `https://your-url.a.run.app/`
- **API Docs:** `https://your-url.a.run.app/docs`
- **Health:** `https://your-url.a.run.app/health`

---

## Advanced: Deploy Using gcloud CLI

```bash
# 1. Install gcloud CLI
# Download: https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth login

# 3. Set project
gcloud config set project MY_PROJECT_ID

# 4. Deploy from GitHub
gcloud run deploy blood-report-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 5. Set environment variables
gcloud run services update blood-report-ai \
  --set-env-vars="GEMINI_API_KEY=your_key,OPENAI_API_KEY=your_key" \
  --region us-central1
```

---

## Cloud Run Features

### ✅ Automatic Scaling
- 0 instances when no requests
- Auto-scales to handle traffic
- Scales down when idle (no idle cost!)

### ✅ Built-in Monitoring
- Cloud Logging: All container logs
- Cloud Trace: Request tracing
- Cloud Monitoring: Metrics & alerts
- Error Reporting: Automatic error tracking

### ✅ Security
- Encryption in transit (HTTPS)
- Service-to-service authentication
- IAM access control
- DDoS protection included

### ✅ Auto-Deploy from GitHub
- Push to main branch
- Cloud Build automatically builds
- New version deployed instantly
- Gradual traffic shifting (canary deployments)

---

## Pricing Calculator

### Free Tier (Always Included):
- ✅ 2 million requests/month (free)
- ✅ 360,000 GB-seconds/month compute (free)
- ✅ 1 GB outbound traffic/month (free)

### After Free Tier:
- **Request:** $0.40 per 1 million requests
- **Compute:** $0.0000247 per 1 GB-second
- **Outbound:** $0.12 per GB (after 1GB free)

### Estimated Cost for 24/7 Usage:
- **Low traffic:** $10-20/month
- **Medium traffic:** $20-50/month
- **High traffic:** $50+/month

---

## Troubleshooting

### Deployment Fails at Build Stage
1. Check Cloud Build logs:
   - Go to: **Cloud Run → Service → Build details**
2. Common issues:
   - Dockerfile has errors (check syntax)
   - Missing files in repository
   - API not enabled
3. Solution: Push to GitHub again to trigger rebuild

### App Crashes at Runtime
1. Check Cloud Logging:
   - Go to: **Logs → Cloud Run logs**
2. Look for Python errors
3. Verify environment variables are set
4. Check Dockerfile exposes correct port

### Can't Connect to Database
- Ensure SQLite file path is `/tmp/` (Cloud Run uses ephemeral storage)
- For persistent data, use Cloud SQL instead

### CORS Issues
- Cloud Run auto-handles CORS properly
- Verify FastAPI CORS middleware settings

---

## Comparison: Cloud Run vs Others

| Feature | Cloud Run | Railway | Render |
|---------|-----------|---------|--------|
| **Free Tier** | Generous | None | Limited |
| **Pay Only Used** | ✅ Yes | No | No |
| **Auto-scaling** | ✅ Excellent | Good | Good |
| **Cold Start** | ~1-2s | None | None |
| **Monitoring** | ✅ Best-in-class | Built-in | Built-in |
| **Cost (24/7)** | $10-20 | $5-10 | ~$72 |
| **Best For** | Scalable apps | Simple projects | Always-on services |

---

## Setup Auto-Deploy from GitHub

1. **Via Cloud Build:**
   - Go: **Cloud Build → Triggers**
   - Create trigger: Point to your repo
   - Branch: `main`
   - Build config: `Dockerfile`
   - Save trigger

2. **Then:**
   - Every push to main automatically:
     - Builds Docker image
     - Deploys to Cloud Run
     - New version live in 2-5 minutes

3. **Gradual Rollout:**
   - Cloud Run supports traffic splitting
   - Send 10% to new version first
   - If healthy, shift remaining traffic
   - Instant rollback if needed

---

## Optional: Custom Domain

1. Go: **Cloud Run service → Manage custom domains**
2. Click: **"Add mapping"**
3. Enter your domain: `blood-report-ai.yourdomain.com`
4. Cloud Run provides CNAME record
5. Add to your DNS provider
6. Auto HTTPS certificate (free)

---

## Monitoring Dashboard

After deployment, view:

**Cloud Console → Cloud Run:**
- Service details
- Metrics (requests, latency, errors)
- Logs (all requests and errors)
- Revisions (version history)
- Traffic splitting (canary deployments)

---

## Next Steps

1. ✅ Deploy to Cloud Run
2. ✅ Test your live URL
3. ✅ Upload blood report image
4. ✅ Check logs in Cloud Logging
5. ✅ Set custom domain (optional)
6. ✅ Monitor metrics automatically
7. ✅ Share your URL!

---

## Comparison: All 3 Options

| Platform | Setup Time | Cost (24/7) | Complexity | Best For |
|----------|-----------|------------|-----------|----------|
| **Railway** | 5 min | $5-10 | Very easy | Beginners |
| **Render** | 5 min | $0-72 | Very easy | Mid-range |
| **Cloud Run** | 10 min | $10-20 | Easy | Scaling apps |

---

## Quick Links

- **Cloud Run Docs:** https://cloud.google.com/run/docs
- **Cloud Console:** https://console.cloud.google.com
- **Pricing Calculator:** https://cloud.google.com/products/calculator
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Your Repo:** https://github.com/loghithakshan/INBLOODO-AGENT26

---

**Cloud Run deployment is production-ready!** 🚀
