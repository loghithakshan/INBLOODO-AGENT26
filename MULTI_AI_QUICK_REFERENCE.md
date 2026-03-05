# 🤖 Multi-AI System - Quick Reference Card

## 60-Second Overview

```
What:   Analyze blood reports with 4 AI models simultaneously
Why:    Get multiple perspectives + best result automatically selected
How:    Call /api/analyze-multi-ai/ endpoint
Result: Recommendations + all AI results + confidence scores
```

---

## 3 Endpoints That Matter

### 1️⃣ Upload & Analyze (Your Report)
```bash
POST /api/analyze-multi-ai/
Required: API Key, Blood Report File
Returns:  Best recommendations + all AI results
Speed:    ~15 seconds
```

### 2️⃣ Demo Test (No Auth Needed)
```bash
GET /api/demo/analyze-multi-ai/{type}
Types:    healthy, prediabetic, high_cholesterol, anemia
Returns:  Complete analysis with all AIs
Speed:    ~15 seconds
```

### 3️⃣ Check Providers
```bash
GET /api/multi-ai/providers
Returns:  Which AIs are available
Speed:    <1 second
```

---

## Copy-Paste Commands

### Test Demo (No Auth)
```bash
curl http://localhost:8000/api/demo/analyze-multi-ai/healthy
```

### Check Available AIs
```bash
curl http://localhost:8000/api/multi-ai/providers
```

### Upload Your Report (Replace TOKEN)
```bash
curl -X POST http://localhost:8000/api/analyze-multi-ai/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@blood_report.pdf"
```

### Send JSON Data
```bash
curl -X POST http://localhost:8000/api/analyze-multi-ai/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"glucose": 120, "cholesterol": 200}'
```

---

## Setup (One Time)

```bash
# 1. Edit .env file
vim .env

# 2. Add API keys
GEMINI_API_KEY=your-key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key

# 3. Restart server
START_FAST.bat

# 4. Test
curl http://localhost:8000/api/multi-ai/providers
```

---

## Response Structure

```json
{
  "recommendations": [
    "AI-selected best recommendations"
  ],
  "processing_time": 14.3,
  
  "multi_ai_results": {
    "gemini": {
      "success": true,
      "confidence": 0.95,       ← 95% confident
      "execution_time": 8.2     ← Execution time
    },
    "openai": {...},
    "claude": {...},
    "grok": {...}
  }
}
```

---

## What Each AI Does

| AI | Speed | Specialty |
|----|-------|-----------|
| 🔵 **Gemini** | ~8s | General analysis |
| 🟢 **OpenAI** | ~10s | Detailed reasoning |
| 💬 **Claude** | ~9s | Thoughtful response |
| ✨ **Grok** | ~11s | Next-gen perspective |

**Winner:** Highest confidence + fastest

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No providers available" | Set API keys in `.env`, restart |
| "API key error" | Check key spelling, ensure not expired |
| "Slow response" | First request slower; cache helps 2nd time |
| "One AI failed" | System uses others automatically |
| "Different results" | Normal! Different AIs = different perspectives |

---

## Performance

```
First Request:      ~15 seconds (full analysis)
Cached Request:     ~0.001 seconds (instant!)
Speedup:            15,000x faster!

Parallel AIs:       11 seconds (vs 38s sequential)
Speedup:            3.5x faster!
```

---

## Example Response

```json
{
  "status": "success",
  "recommendations": [
    "🩺 Consult endocrinologist for glucose management",
    "📊 Monitor blood sugar levels weekly"
  ],
  "processing_time": 14.3,
  "multi_ai_results": {
    "gemini": {
      "success": true,
      "confidence": 0.95,
      "recommendations": ["Consult endocrinologist..."],
      "execution_time": 8.2
    },
    "openai": {
      "success": true,
      "confidence": 0.88,
      "recommendations": ["Monitor glucose..."],
      "execution_time": 10.1
    }
  }
}
```

---

## Key Features

✅ **4 AIs in Parallel**  - Gemini, OpenAI, Claude, Grok  
✅ **Automatic Selection** - Best AI chosen automatically  
✅ **Confidence Scores** - Know how confident each is  
✅ **Full Transparency** - See all results + reasoning  
✅ **Fast Execution** - Parallel = faster than sequential  
✅ **Smart Fallback** - If one fails, uses others  
✅ **Caching** - 2nd request instant  

---

## File Types Supported

✅ PDF  
✅ PNG, JPG, JPEG  
✅ CSV  
✅ JSON  
✅ TXT  
✅ TIFF, BMP, WEBP  

---

## Python Integration

```python
import requests

api = "http://localhost:8000/api/analyze-multi-ai/"
key = "YOUR_API_KEY"

# Option 1: File
with open("report.pdf", "rb") as f:
    response = requests.post(
        api,
        files={"file": f},
        headers={"Authorization": f"Bearer {key}"}
    )

# Option 2: JSON
response = requests.post(
    api,
    json={"glucose": 120, "cholesterol": 200},
    headers={"Authorization": f"Bearer {key}"}
)

result = response.json()
print(result["recommendations"])  # Best result
print(result["multi_ai_results"]) # All results
```

---

## API Keys to Get

| Provider | Link | Free? |
|----------|------|-------|
| Google Gemini | console.cloud.google.com | ✅ Yes |
| OpenAI | platform.openai.com | ✅ Free tier |
| Anthropic Claude | console.anthropic.com | ✅ Free tier |
| xAI Grok | console.x.ai | Requirements vary |

---

## Documentation Links

| Link | Purpose |
|------|---------|
| `MULTI_AI_COMPARISON_GUIDE.md` | Complete guide |
| `MULTI_AI_QUICK_START.md` | Setup guide |
| `MULTI_AI_INTEGRATION_GUIDE.md` | Developer guide |

---

## URLs to Bookmark

```
Dashboard:    http://localhost:8000
API Docs:     http://localhost:8000/docs
Health Check: http://localhost:8000/health
Demo:         http://localhost:8000/api/demo/analyze-multi-ai/healthy
Providers:    http://localhost:8000/api/multi-ai/providers
```

---

## Success Checklist

- ✅ API keys set in `.env`
- ✅ Server restarted (`START_FAST.bat`)
- ✅ Demo test works (`curl .../healthy`)
- ✅ Providers visible (`curl .../providers`)
- ✅ File uploaded successfully
- ✅ All 4 AIs returned results
- ✅ Best AI selected
- ✅ Confidence scores visible

---

## Quick Start (Copy-Paste)

### Step 1: Edit .env
```env
GEMINI_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
```

### Step 2: Restart
```bash
START_FAST.bat
```

### Step 3: Test
```bash
curl http://localhost:8000/api/demo/analyze-multi-ai/healthy
```

### Step 4: Upload
```bash
curl -X POST http://localhost:8000/api/analyze-multi-ai/ \
  -H "Authorization: Bearer YOUR_KEY" \
  -F "file=@blood_report.pdf"
```

**Done!** 🎉

---

## Common Questions

**Q: How long does analysis take?**  
A: ~15 seconds (4 AIs in parallel). 2nd request instant (cached).

**Q: Which AI is fastest?**  
A: Gemini usually (~8s). System picks best overall, not just fastest.

**Q: What if API key fails?**  
A: System automatically uses next available AI.

**Q: Can I use just one AI?**  
A: Yes, use `/api/demo/analyze-json/` for single AI.

**Q: Is data stored?**  
A: Only in output (parameters + recommendations). No raw data retention.

---

## Keyboard Shortcuts

| Action | Command |
|--------|---------|
| Test Demo | `curl .../healthy` |
| Check Status | `curl .../providers` |
| Quick Health | `curl .../health` |
| API Docs | `localhost:8000/docs` |

---

## Time-Saving Tips

1. **Save cURL commands** to file for quick testing
2. **Set API_KEY env var** to avoid typing Bearer token
3. **Bookmark demo endpoint** for quick tests
4. **Use cache** - same analysis = instant results
5. **Monitor logs** - see what each AI is doing

---

## Before Going Live

- ✅ Test all 4 AIs work
- ✅ Check response time acceptable
- ✅ Verify confidence scores reasonable
- ✅ Review AI selection logic
- ✅ Test fallback scenarios
- ✅ Monitor performance metrics
- ✅ Set up logging

---

## When Something's Wrong

1. **Check API keys** - Most common issue
2. **Check logs** - See detailed errors
3. **Test providers** - `GET /api/multi-ai/providers`
4. **Check network** - Verify internet connection
5. **Restart server** - Clear any cached state

---

**Print this card | Bookmark it | Share it! 📋**

For full docs: See `MULTI_AI_COMPARISON_GUIDE.md`  
Quick setup: See `MULTI_AI_QUICK_START.md`  
Development: See `MULTI_AI_INTEGRATION_GUIDE.md`
