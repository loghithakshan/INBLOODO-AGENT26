# 🤖 Multi-AI Integration Guide for Developers

## System Architecture

```
Your Application
      ↓
[API Endpoint] /api/analyze-multi-ai/
      ↓
[Multi-Agent Orchestrator]
      ├→ Parameter Extraction
      ├→ Parameters Interpretation
      ├→ Risk Analysis
      ├→ Prediction
      │
      └→ [Multi-AI Comparison Agent] ← NEW
            ├→ Run Gemini (thread 1)
            ├→ Run OpenAI (thread 2)
            ├→ Run Claude (thread 3)
            └→ Run Grok (thread 4)
            
            ↓
            Score & Compare Results
            ↓
            Select Best AI
            ↓
      [Return All Results + Best Selection]
      ↓
Your Application
```

---

## Code Integration

### Method 1: Direct HTTP API (Recommended for External Apps)

```python
import requests
import json

class MultiAIAnalyzer:
    def __init__(self, api_url="http://localhost:8000", api_key="YOUR_KEY"):
        self.api_url = api_url
        self.api_key = api_key
    
    def analyze_file(self, file_path):
        """Analyze blood report file with multi-AI comparison"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            
            response = requests.post(
                f"{self.api_url}/api/analyze-multi-ai/",
                files=files,
                headers=headers
            )
            
            return response.json()
    
    def analyze_json(self, parameters):
        """Analyze JSON blood parameters with multi-AI"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        response = requests.post(
            f"{self.api_url}/api/analyze-multi-ai/",
            json=parameters,
            headers=headers
        )
        
        return response.json()
    
    def get_providers_status(self):
        """Check which AI providers are available"""
        response = requests.get(f"{self.api_url}/api/multi-ai/providers")
        return response.json()


# Usage
analyzer = MultiAIAnalyzer(api_key="your-api-key")

# Analyze file
result = analyzer.analyze_file("blood_report.pdf")
print(f"Best recommendations: {result['recommendations']}")
print(f"All AI results: {result['multi_ai_results']}")

# Check providers
providers = analyzer.get_providers_status()
print(f"Available AIs: {providers['available_providers']}")
```

### Method 2: Direct Python Module (For Internal Apps)

```python
from src.agent.agent_orchestrator import MultiAgentOrchestrator
from src.llm.multi_ai_comparison import get_multi_ai_service
import asyncio

async def analyze_with_all_ais(blood_parameters):
    """Direct Python integration - no HTTP overhead"""
    
    orchestrator = MultiAgentOrchestrator()
    
    # Execute with multi-AI comparison
    report = await orchestrator.execute_with_multi_ai(
        raw_params=blood_parameters,
        patient_context=None
    )
    
    # Access results
    print(f"Best recommendations: {report.recommendations}")
    print(f"All AI results: {report.multi_ai_results}")
    print(f"Timestamp: {report.timestamp}")
    
    return report


# Usage
parameters = {
    "glucose": 120,
    "cholesterol": 200,
    "hdl": 50,
    "ldl": 130,
    "triglycerides": 150,
    "hemoglobin": 14.5,
    "hematocrit": 43,
    "white_blood_cells": 7.2,
    "platelets": 250
}

report = asyncio.run(analyze_with_all_ais(parameters))
```

### Method 3: Service Layer Pattern

```python
from dataclasses import dataclass
from typing import Dict, List
from src.llm.multi_ai_comparison import (
    get_multi_ai_service, 
    ComparisonResult
)

@dataclass
class HealthAnalysisRequest:
    parameters: Dict[str, float]
    patient_id: str
    timestamp: str

@dataclass  
class HealthAnalysisResponse:
    patient_id: str
    best_recommendations: List[str]
    all_ai_results: Dict
    confidence_score: float
    analysis_time: float

class HealthAnalysisService:
    def __init__(self):
        self.multi_ai_service = get_multi_ai_service()
    
    def analyze_health_data(self, request: HealthAnalysisRequest) -> HealthAnalysisResponse:
        """Service method for health analysis"""
        
        # You would extract interpretations and risks here
        interpretations = self._extract_interpretations(request.parameters)
        risks = self._extract_risks(request.parameters)
        
        # Compare all AIs
        comparison: ComparisonResult = self.multi_ai_service.compare_ai_results(
            interpretations=interpretations,
            risks=risks,
            parameters=request.parameters
        )
        
        # Build response
        return HealthAnalysisResponse(
            patient_id=request.patient_id,
            best_recommendations=comparison.best_result,
            all_ai_results=comparison.all_results,
            confidence_score=self._calculate_confidence(comparison),
            analysis_time=self._calculate_time(comparison)
        )
    
    def _extract_interpretations(self, params: Dict) -> List[str]:
        """Extract interpretations from parameters"""
        # Your interpretation logic
        return []
    
    def _extract_risks(self, params: Dict) -> List[str]:
        """Extract risks from parameters"""
        # Your risk analysis logic
        return []


# Usage
service = HealthAnalysisService()
request = HealthAnalysisRequest(
    parameters={"glucose": 120, "cholesterol": 200},
    patient_id="P123",
    timestamp="2026-03-01T10:30:00Z"
)
response = service.analyze_health_data(request)
print(f"Best recommendations: {response.best_recommendations}")
```

---

## Extending the System

### Create Custom AI Provider

```python
from src.llm.llm_provider import LLMProvider
from typing import List, Dict, Any, Optional

class CustomAIProvider(LLMProvider):
    """Custom AI provider for integration"""
    
    def __init__(self):
        self.name = "Custom AI"
        self.available = False
        self.initialize()
    
    def initialize(self) -> bool:
        """Initialize custom AI"""
        try:
            # Your initialization logic
            self.api_key = os.getenv("CUSTOM_AI_KEY")
            if self.api_key:
                self.available = True
                return True
        except Exception as e:
            logger.error(f"Custom AI init failed: {e}")
        return False
    
    def is_available(self) -> bool:
        return self.available
    
    def generate_recommendations(
        self,
        interpretations: List[str],
        risks: List[str],
        parameters: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate recommendations"""
        try:
            # Your API call logic
            prompt = self._build_prompt(interpretations, risks, parameters)
            
            # Call your AI service
            response = self._call_api(prompt)
            
            # Parse response
            recommendations = self._parse_response(response)
            
            return recommendations
        except Exception as e:
            logger.error(f"Custom AI failed: {e}")
            return []
    
    def _build_prompt(self, interp, risks, params) -> str:
        return "Your prompt here"
    
    def _call_api(self, prompt: str) -> str:
        return "API response"
    
    def _parse_response(self, response: str) -> List[str]:
        return response.split('\n')
```

Register your custom provider:

```python
# In src/llm/multi_ai_comparison.py
from src.llm.custom_ai import CustomAIProvider

# Add to _initialize_providers:
("custom", CustomAIProvider()),
```

---

## Real-World Integration Examples

### Example 1: Web Application

```python
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/health/analyze")
async def analyze_health(file: UploadFile = File(...)):
    """Health analysis endpoint with multi-AI comparison"""
    
    # Read file
    content = await file.read()
    
    # Extract parameters
    params = extract_parameters(content, file.filename)
    
    # Use multi-AI service
    service = HealthAnalysisService()
    result = service.analyze_health_data(params)
    
    return {
        "best_recommendations": result.best_recommendations,
        "all_results": result.all_ai_results,
        "confidence": result.confidence_score
    }
```

### Example 2: CLI Tool

```python
import click
from pathlib import Path

@click.command()
@click.option('--file', type=Path, required=True, help='Blood report file')
@click.option('--format', default='json', help='Output format')
def analyze_report(file: Path, format: str):
    """CLI tool for blood report analysis"""
    
    # Load parameters
    params = load_parameters(file)
    
    # Analyze
    analyzer = MultiAIAnalyzer()
    result = analyzer.analyze_json(params)
    
    # Output
    if format == 'json':
        click.echo(json.dumps(result, indent=2))
    else:
        display_results(result)

if __name__ == '__main__':
    analyze_report()
```

Run: `python cli.py --file blood_report.pdf`

### Example 3: Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def batch_analyze_reports(report_dir: str, num_workers: int = 4):
    """Analyze multiple reports in parallel"""
    
    analyzer = MultiAIAnalyzer()
    reports = Path(report_dir).glob("*.pdf")
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(analyzer.analyze_file, str(f)): f.name 
            for f in reports
        }
        
        for future in futures:
            filename = futures[future]
            try:
                result = future.result(timeout=60)
                results[filename] = result
            except Exception as e:
                results[filename] = {"error": str(e)}
    
    return results


# Usage
batch_results = batch_analyze_reports("./blood_reports/", num_workers=8)

for filename, result in batch_results.items():
    print(f"{filename}: {result['overall_risk']}")
```

### Example 4: Database Integration

```python
from sqlalchemy import Column, String, JSON, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class HealthAnalysis(Base):
    __tablename__ = "health_analyses"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    parameters = Column(JSON)
    best_recommendations = Column(JSON)
    
    # Store all AI results
    gemini_result = Column(JSON)
    openai_result = Column(JSON)
    claude_result = Column(JSON)
    grok_result = Column(JSON)
    
    # Metadata
    selected_provider = Column(String)
    confidence_score = Column(Float)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

def save_analysis_results(db, patient_id: str, result: dict):
    """Save multi-AI analysis to database"""
    
    analysis = HealthAnalysis(
        patient_id=patient_id,
        parameters=result['extracted_parameters'],
        best_recommendations=result['recommendations'],
        
        # Store individual AI results
        gemini_result=result['multi_ai_results'].get('gemini'),
        openai_result=result['multi_ai_results'].get('openai'),
        claude_result=result['multi_ai_results'].get('claude'),
        grok_result=result['multi_ai_results'].get('grok'),
        
        # Metadata
        selected_provider=result.get('best_provider'),
        confidence_score=0.9,  # Calculate from results
        processing_time=result['processing_time']
    )
    
    db.add(analysis)
    db.commit()
```

---

## Performance Optimization

### Caching Results

```python
from functools import lru_cache
import hashlib
import json

class CachedMultiAIAnalyzer:
    @lru_cache(maxsize=1000)
    def analyze_cached(self, params_hash: str):
        """Cache expensive multi-AI analysis"""
        pass
    
    def analyze_with_cache(self, parameters: Dict):
        """Analyze with automatic caching"""
        # Hash parameters
        params_str = json.dumps(parameters, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        
        # Try cache
        cached = self.analyze_cached(params_hash)
        if cached:
            return cached
        
        # If not cached, analyze
        result = self.analyzer.analyze_json(parameters)
        
        # Cache for future
        self._cache_result(params_hash, result)
        
        return result
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

async def analyze_multiple_patients(patients: List[Dict]):
    """Process multiple patients with multi-AI in parallel"""
    
    analyzer = MultiAIAnalyzer()
    
    tasks = [
        asyncio.to_thread(
            analyzer.analyze_json, 
            patient['parameters']
        )
        for patient in patients
    ]
    
    results = await asyncio.gather(*tasks)
    
    return results
```

---

## Testing

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch

def test_multi_ai_comparison():
    """Test multi-AI comparison"""
    
    # Setup
    parameters = {"glucose": 120, "cholesterol": 200}
    
    # Execute
    analyzer = MultiAIAnalyzer()
    result = analyzer.analyze_json(parameters)
    
    # Assert
    assert result['status'] == 'success'
    assert 'multi_ai_results' in result
    assert len(result['recommendations']) > 0

def test_provider_fallback():
    """Test fallback when AI fails"""
    
    with patch('requests.post') as mock:
        # Simulate AI failure
        mock.side_effect = Exception("API Error")
        
        analyzer = MultiAIAnalyzer()
        # Should use fallback
        result = analyzer.analyze_json({"glucose": 120})
        
        assert result['status'] == 'success'  # Fallback worked
```

---

## Monitoring & Logging

```python
import logging

logger = logging.getLogger(__name__)

class MonitoredMultiAIAnalyzer:
    def analyze_with_monitoring(self, parameters):
        """Analyze with comprehensive monitoring"""
        
        start_time = time.time()
        
        try:
            logger.info(f"Starting analysis for {len(parameters)} parameters")
            
            result = self.analyzer.analyze_json(parameters)
            
            elapsed = time.time() - start_time
            
            # Log success
            logger.info(
                f"Analysis completed in {elapsed:.2f}s",
                extra={
                    "processing_time_ms": elapsed * 1000,
                    "ai_count": len(result.get('multi_ai_results', {})),
                    "recommendations": len(result.get('recommendations', []))
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            raise
```

---

## Deployment Considerations

1. **Environment Separation**
   ```bash
   # Development
   ENVIRONMENT=development
   
   # Production
   ENVIRONMENT=production
   LOG_LEVEL=warning
   ```

2. **API Key Management**
   ```bash
   # Use secrets manager, not .env in production
   source /var/secrets/ai_keys.sh
   ```

3. **Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @limiter.limit("10/minute")
   @app.post("/api/analyze-multi-ai/")
   async def analyze(...):
       pass
   ```

4. **Monitoring**
   ```python
   # Use Prometheus/Datadog
   metrics = {
       "analyses_total": Counter(...),
       "analysis_duration_seconds": Histogram(...),
       "ai_failures": Counter(...)
   }
   ```

---

## Support & Resources

- **Full API Docs:** [MULTI_AI_COMPARISON_GUIDE.md](MULTI_AI_COMPARISON_GUIDE.md)
- **Quick Start:** [MULTI_AI_QUICK_START.md](MULTI_AI_QUICK_START.md)
- **Source Code:** `src/llm/multi_ai_comparison.py`
- **Agent Code:** `src/agent/agent_orchestrator.py`

---

Happy integrating! 🚀
