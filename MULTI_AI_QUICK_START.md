# 🤖 Multi-AI Comparison - Quick Start

## 30-Second Setup

### 1. Add API Keys to `.env`

```bash
# .env file
GEMINI_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
GROK_API_KEY=your-key-here (optional)
```

### 2. Restart Server

```bash
START_FAST.bat    # or python main.py
```

### 3. Test Demo (No Auth Required)

```bash
curl http://localhost:8000/api/demo/analyze-multi-ai/healthy
```

**That's it!** You now have multi-AI comparison running.

---

## Test Immediately

### Test 1: Check Available AIs
```bash
curl http://localhost:8000/api/multi-ai/providers
```

Shows which AIs are configured and working.

### Test 2: Demo Analysis
```bash
# Healthy sample
curl http://localhost:8000/api/demo/analyze-multi-ai/healthy

# Prediabetic sample
curl http://localhost:8000/api/demo/analyze-multi-ai/prediabetic

# High cholesterol
curl http://localhost:8000/api/demo/analyze-multi-ai/high_cholesterol

# Anemia
curl http://localhost:8000/api/demo/analyze-multi-ai/anemia
```

### Test 3: Upload Your Own Report
```bash
curl -X POST http://localhost:8000/api/analyze-multi-ai/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@blood_report.pdf"
```

---

## What You'll See

### Response Structure

```json
{
  "status": "success",
  "recommendations": [
    "AI-selected best recommendations here"
  ],
  "processing_time": 14.3,
  
  "multi_ai_results": {
    "gemini": {
      "success": true,
      "confidence": 95,
      "execution_time": 8.2
    },
    "openai": {
      "success": true,
      "confidence": 88,
      "execution_time": 10.1
    },
    "claude": {
      "success": true,
      "confidence": 85,
      "execution_time": 9.5
    }
  }
}
```

### In Logs, You'll See

```
[INFO] 🤖 Starting Multi-AI Comparison with 12 parameters...
[INFO]   ✓ gemini: 3 recommendations (0.95s)
[INFO]   ✓ openai: 3 recommendations (1.01s)
[INFO]   ✓ claude: 3 recommendations (0.95s)
[INFO] 🏆 Best provider: gemini
[INFO] ✅ Multi-AI comparison completed in 10.2s
```

---

## Expected Behavior

### ✅ All AIs Working
Each AI runs in parallel, shows in response with confidence scores.

### ✅ Some AIs Failing
System automatically uses others. Fallback AI always available.

### ✅ Different Results from Each AI
**This is normal!** That's why multi-AI is powerful:
- Gemini might focus on glucose
- OpenAI might emphasize cholesterol
- Claude might provide more detailed reasoning
- System picks best overall result

### ✅ First Run Slower
First analysis: 15-20s  
Cached analysis: 0.001s (25,000x faster!)

---

## Troubleshooting

### "No LLM providers available"
Missing API keys. **Solution:** Set API keys in .env and restart.

### "Grok API failed"
Grok might not be configured. **Solution:** System automatically uses other AIs.

### Very Slow Response
Check if network is slow. **Solution:** Response cache helps second time.

### Different Results Each Time
Normal behavior! LLMs have slight randomness. **Solution:** Use multiple requests for consistency.

---

## API Endpoints Quick Reference

| Endpoint | Auth | Use Case |
|----------|------|----------|
| `/api/analyze-multi-ai/` | Required | Upload & analyze |
| `/api/demo/analyze-multi-ai/{type}` | None | Test with samples |
| `/api/multi-ai/providers` | None | Check available AIs |

**Sample types:** `healthy`, `prediabetic`, `high_cholesterol`, `anemia`

---

## Full Python Example

```python
import requests
import json

def test_multi_ai():
    # Test 1: Check available providers
    print("📋 Checking available AI providers...")
    resp = requests.get("http://localhost:8000/api/multi-ai/providers")
    print(f"Available: {resp.json()['available_providers']}\n")
    
    # Test 2: Demo analysis
    print("📊 Running demo analysis (prediabetic sample)...")
    resp = requests.get(
        "http://localhost:8000/api/demo/analyze-multi-ai/prediabetic"
    )
    data = resp.json()
    
    # Show results
    print(f"✅ Status: {data['status']}")
    print(f"⏱️  Processing time: {data['processing_time']:.1f}s")
    print(f"\n🤖 AI Results:")
    
    for ai, result in data.get('all_ai_results', {}).items():
        status = "✓" if result['success'] else "✗"
        print(f"  {status} {ai.upper()}: {result['confidence']}% confidence")
    
    # Show recommendations
    print(f"\n📝 Best Recommendations:")
    for i, rec in enumerate(data.get('recommendations', [])[:3], 1):
        print(f"  {i}. {rec}")

if __name__ == "__main__":
    test_multi_ai()
```

**Output:**
```
📋 Checking available AI providers...
Available: ['gemini', 'openai', 'claude']

📊 Running demo analysis (prediabetic sample)...
✅ Status: success
⏱️  Processing time: 14.3s

🤖 AI Results:
  ✓ GEMINI: 95% confidence
  ✓ OPENAI: 88% confidence
  ✓ CLAUDE: 85% confidence

📝 Best Recommendations:
  1. 🩺 Consult endocrinologist for glucose management
  2. 📊 Monitor blood sugar weekly
  3. 🥗 Reduce refined carbohydrates
```

---

## Performance Tips

### 1. **Use Cache**
First request: 15-20s  
Repeated request (cached): 0.001s

### 2. **Disable Slow AIs** (Optional)
If an AI is slow, remove its API key from .env

### 3. **Use Parallel Processing**
System already runs AIs in parallel (3x faster than sequential)

### 4. **Pre-warm Cache**
Make first call before heavy usage

---

## Configuration File Example

Save as `.env`:

```env
# ==================== Multi-AI Configuration ====================

# Google Gemini
GEMINI_API_KEY=AIzaSyD...your-key-here

# OpenAI
OPENAI_API_KEY=sk-proj-...your-key-here

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...your-key-here

# xAI Grok (optional)
GROK_API_KEY=grok-...your-key-here

# ==================== Server Configuration ====================
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# ==================== API Configuration ====================
API_KEY=your-secret-api-key-12345

# ==================== Database ====================
DATABASE_URL=sqlite:///blood_reports.db
```

---

## Next Steps

1. ✅ Set API keys in `.env`
2. ✅ Run `START_FAST.bat` to restart server
3. ✅ Test `/api/multi-ai/providers` endpoint
4. ✅ Try demo: `/api/demo/analyze-multi-ai/healthy`
5. ✅ Upload real blood report to `/api/analyze-multi-ai/`
6. ✅ Review all AI results in response
7. ✅ Check which AI was selected as "best"
8. ✅ Use insights for your health decisions

---

## Support

**Health Check:**
```bash
curl http://localhost:8000/health
```

**API Documentation:**
```
http://localhost:8000/docs
```

**Quick Test:**
```bash
curl http://localhost:8000/api/demo/analyze-multi-ai/healthy
```

---

**Ready to use multi-AI power! 🚀**

Start with: `curl http://localhost:8000/api/demo/analyze-multi-ai/healthy`
