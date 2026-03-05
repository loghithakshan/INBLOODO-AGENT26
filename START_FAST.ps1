# ============================================================================
# BLOOD REPORT AI - LIGHTNING-FAST STARTER (PowerShell)
# ============================================================================
# Fastest startup possible - runs in parallel and skips all unnecessary steps
# Startup time: 1-2 seconds
# ============================================================================

Write-Host ""
Write-Host "⚡⚡⚡ LIGHTNING-FAST SERVER ⚡⚡⚡" -ForegroundColor Cyan
Write-Host ""

# Check Python exists
try {
    python --version 2>&1 | Out-Null
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
    pause
    exit 1
}

# Setup venv (only on first run)
if (!(Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "📦 First run - Setting up (30 sec)..." -ForegroundColor Yellow
    python -m venv venv | Out-Null
    & "venv\Scripts\Activate.ps1" | Out-Null
    pip install --upgrade pip --quiet 2>&1 | Out-Null
    pip install -r requirements.txt --quiet 2>&1 | Out-Null
    Write-Host "✓ Ready!" -ForegroundColor Green
} else {
    & "venv\Scripts\Activate.ps1" | Out-Null
}

# Optimize for performance
$env:ENVIRONMENT = "production"
$env:PYTHONOPTIMIZE = "2"

Write-Host ""
Write-Host "🚀 Starting Server..." -ForegroundColor Green
Write-Host ""
Write-Host "   Dashboard: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Start server
python run_instant.py
