# 🚀 CLOUD DEPLOYMENT GUIDE - INBLOODO AGENT

**Status**: Production-ready for cloud deployment  
**Supported Platforms**: Render, Heroku, AWS, GCP, Azure

---

## 1️⃣ RENDER.COM DEPLOYMENT (EASIEST) ✅

### **Step 1: Connect Repository**
```
1. Go to render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select branch: main
```

### **Step 2: Configure Service**
```
Name:             inbloodo-agent
Runtime:          Python 3.12
Build Command:    pip install -r requirements.txt
Start Command:    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --timeout 120
```

### **Step 3: Environment Variables**
```
ENVIRONMENT=production
HOST=0.0.0.0
PORT=10000
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=generate_a_random_key
```

### **Step 4: Add PostgreSQL Database**
```
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Name: blood_reports_db
4. Copy connection string to DATABASE_URL
```

### **Step 5: Deploy**
```
1. Click "Create Web Service"
2. Render automatically deploys on git push
3. Visit https://inbloodo-agent.onrender.com
```

### **Cost**: Free tier available ($0/month)

---

## 2️⃣ HEROKU DEPLOYMENT

### **Step 1: Install Heroku CLI**
```bash
# Windows
choco install heroku-cli

# Or download from heroku.com/download
```

### **Step 2: Login & Create App**
```bash
heroku login
heroku create inbloodo-agent
```

### **Step 3: Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:standard-0
```

### **Step 4: Set Environment Variables**
```bash
heroku config:set ENVIRONMENT=production
heroku config:set GEMINI_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set SECRET_KEY=$(openssl rand -base64 32)
```

### **Step 5: Deploy**
```bash
git push heroku main
```

### **Monitor**
```bash
heroku logs -t              # Live logs
heroku ps                   # Dyno status
heroku open                 # Open app in browser
```

### **Cost**: $7/month minimum (free tier deprecated)

---

## 3️⃣ AWS DEPLOYMENT

### **Option A: EC2 + RDS**

**Step 1: Create EC2 Instance**
```bash
# Launch t3.micro instance (free tier eligible)
# OS: Ubuntu 22.04 LTS
# Security Group: Allow ports 80, 443, 8000
```

**Step 2: Connect via SSH**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.12 python3-pip git postgresql-client

# Clone repository
git clone https://github.com/yourusername/blood-report-ai.git
cd blood-report-ai

# Install Python packages
pip install -r requirements.txt
```

**Step 3: Create RDS Database**
```bash
# AWS Console → RDS → Create Database
# Engine: PostgreSQL
# Instance class: db.t3.micro (free tier)
# Get connection string
```

**Step 4: Configure & Run**
```bash
# Create .env file
export GEMINI_API_KEY=your_key
export OPENAI_API_KEY=your_key
export DATABASE_URL=postgresql://user:pass@rds-endpoint/db

# Start application
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

**Step 5: Setup Nginx Reverse Proxy**
```bash
sudo apt install nginx

# Create / config file
sudo nano /etc/nginx/sites-available/inbloodo

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/inbloodo /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

**Step 6: Enable HTTPS**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### **Cost**: $0-5/month with free tier

---

### **Option B: AWS Lambda (Serverless)**

```bash
# Install SAM CLI
pip install aws-sam-cli

# Create template
sam init --runtime python3.12

# Edit template.yaml
# Add FastAPI app as lambda handler
# Deploy
sam deploy --guided
```

### **Cost**: $0/month (free tier for <1M requests)

---

## 4️⃣ GOOGLE CLOUD DEPLOYMENT

### **Step 1: Setup Project**
```bash
gcloud init
gcloud config set project your-project-id
gcloud app create
```

### **Step 2: Create app.yaml**
```yaml
runtime: python312

env: standard

entrypoint: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

env_variables:
  ENVIRONMENT: "production"
  PORT: "8080"

handlers:
  - url: /.*
    script: auto

automatic_scaling:
  min_instances: 0
  max_instances: 5
```

### **Step 3: Deploy**
```bash
gcloud app deploy

# View logs
gcloud app logs read -f
```

### **Cost**: Free tier available

---

## 5️⃣ AZURE DEPLOYMENT

### **Step 1: Install Azure CLI**
```bash
choco install azure-cli
az login
```

### **Step 2: Create Resource Group**
```bash
az group create -n inbloodo -l eastus
```

### **Step 3: Create App Service**
```bash
az appservice plan create -n inbloodo-plan -g inbloodo -sku B1
az webapp create -n inbloodo-app -g inbloodo -p inbloodo-plan
```

### **Step 4: Configure & Deploy**
```bash
az webapp deployment source config-zip -g inbloodo -n inbloodo-app --src repo.zip
az webapp config appsettings set -g inbloodo -n inbloodo-app \
  --settings GEMINI_API_KEY=your_key OPENAI_API_KEY=your_key
```

### **Cost**: $10+/month

---

## 📊 COMPARISON TABLE

| Platform | Cost | Ease | Performance | Free Tier |
|----------|------|------|-------------|-----------|
| **Render** | $7+ | ⭐⭐⭐⭐⭐ | Excellent | No |
| **Heroku** | $7+ | ⭐⭐⭐⭐ | Good | No |
| **AWS** | $0-5 | ⭐⭐⭐ | Excellent | Yes |
| **GCP** | $0-5 | ⭐⭐⭐ | Excellent | Yes |
| **Azure** | $10+ | ⭐⭐⭐ | Good | No |

---

## 🔄 DEPLOYMENT CHECKLIST

Before deploying to production:

### API Keys
- [ ] Gemini API key obtained & valid
- [ ] OpenAI API key obtained & valid
- [ ] Anthropic API key obtained & valid
- [ ] All keys stored in environment variables (NOT in code)

### Database
- [ ] PostgreSQL instance created
- [ ] Connection string verified
- [ ] Migrations applied
- [ ] Backups configured

### Security
- [ ] HTTPS/SSL enabled
- [ ] CORS configured for your domain
- [ ] API rate limiting enabled
- [ ] Error messages sanitized
- [ ] Logging configured

### Performance
- [ ] CDN configured (if using static files)
- [ ] Database indexing optimized
- [ ] Caching enabled
- [ ] Monitoring set up

### Monitoring
- [ ] Error tracking enabled (Sentry)
- [ ] Performance monitoring enabled
- [ ] Health checks configured
- [ ] Auto-scaling enabled

---

## 🚀 QUICK DEPLOY SCRIPTS

### **Render Deploy**
```bash
# Just push to GitHub, Render auto-deploys
git add .
git commit -m "Deploy to production"
git push origin main

# Monitor at render.com dashboard
```

### **Heroku Deploy**
```bash
git push heroku main
heroku logs -t
```

### **AWS Deploy**
```bash
sam build
sam deploy --guided
```

### **Docker Deploy** (Any platform)
```bash
docker build -t inbloodo-agent .
docker push your-registry/inbloodo-agent
docker run -p 8000:8000 inbloodo-agent
```

---

## 🛞 Domain & HTTPS

### **Connect Custom Domain**

**Render**:
```
1. Settings → Custom Domain
2. Update DNS records
3. Auto SSL certificate
```

**Heroku**:
```bash
heroku domains:add www.yourdomain.com
# Update DNS CNAME records
```

**AWS**:
```
1. Route 53 → Hosted Zones
2. Create A record pointing to ELB/App
3. Create SSL cert in ACM
```

---

## 📈 SCALING CONSIDERATIONS

### Vertical Scaling
```
Increase machine size/tier for more power
- Render: $103/month for standard tier
- AWS: Upgrade EC2 instance type
- Heroku: Premium dynos
```

### Horizontal Scaling
```
Add multiple instances with load balancer
- Render: Auto-scales based on load
- AWS: Auto Scaling Groups
- GCP: Cloud Run (serverless)
```

### Database Scaling
```
- Read replicas for high traffic
- Connection pooling (pgBouncer)
- Redis caching layer
- Database sharding for massive scale
```

---

## 💰 COST ESTIMATION

### Low Traffic (<10K requests/day)
```
Render Free Tier:      $0/month
PostgreSQL:            $7-15/month
Domain:                $10/month
────────────────────────────────
Total:                 ~$17-25/month
```

### Medium Traffic (10K-100K requests/day)
```
Render Standard:       $7/month
PostgreSQL Standard:   $20/month
Domain + SSL:          $10/month
CDN (optional):        $10-20/month
────────────────────────────────
Total:                 ~$47-57/month
```

### High Traffic (>100K requests/day)
```
Multiple Render:       $28/month
PostgreSQL Pro:        $100+/month
CDN + DDoS:           $50+/month
────────────────────────────────
Total:                 $178+/month
```

---

## 🔍 MONITORING & LOGS

### **Application Monitoring**
```bash
# View live logs
heroku logs -t          # Heroku
gcloud app logs read -f # GCP
azure webapp log tail   # Azure

# Set up error tracking
pip install sentry-sdk
```

### **Performance Monitoring**
```python
# Add to main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

### **Uptime Monitoring**
```
Use StatusPage.io or Upptime
Create health check: https://your-app.com/health
Set alert for downtime
```

---

## ✅ POST-DEPLOYMENT

### Verify Deployment
```bash
# Test health check
curl https://your-app.com/health

# Test analysis endpoint
curl -X POST https://your-app.com/analyze-report/ \
  -H "Content-Type: application/json" \
  -d '{"hemoglobin": 11.5, "glucose": 180, ...}'

# View API docs
https://your-app.com/docs
```

### Configure Backups
```
Database: Daily automated backups
Media: Store in S3/Cloud Storage
Logs: Archive old logs to cold storage
```

### Setup CI/CD
```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: |
          curl -X POST https://api.render.com/deploy/srv-...
```

---

## 🎯 RECOMMENDED SETUP

**For Learning/Testing**:
- ✅ AWS Free Tier (EC2 + RDS)
- ✅ GCP Free Tier (Cloud Run)
- ✅ Heroku (costs but fast setup)

**For Production**:
- ✅ Render (easiest)
- ✅ AWS (most flexible)
- ✅ GCP (best for scale)

**For Enterprise**:
- ✅ AWS (ECS + RDS + CloudFront)
- ✅ GCP (GKE + Cloud SQL)
- ✅ Azure (App Service + SQL Database)

---

**Next Steps**:
1. Choose a platform
2. Set up account
3. Configure environment variables
4. Deploy using guide above
5. Monitor and scale as needed

**Questions**? Check platform documentation or reach out!
