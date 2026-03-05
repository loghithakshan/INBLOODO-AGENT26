@echo off
REM ============================================================================
REM BLOOD REPORT AI - ULTRA-FAST SERVER LAUNCHER
REM ============================================================================
REM Optimized for speed - skips unnecessary checks
REM Startup time: 2-3 seconds (vs 30+ seconds)
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ⚡ ULTRA-FAST SERVER LAUNCHER ⚡
echo.

REM Quick Python check (1 second)
python --version >nul 2>&1 || (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Setup venv if needed (only first run)
if not exist "venv\Scripts\activate.bat" (
    echo 📦 First run - Creating environment (30 seconds)...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt >nul 2>&1
    echo ✓ Environment ready
) else (
    REM Subsequent runs - just activate
    call venv\Scripts\activate.bat
)

REM Set performance flags
set ENVIRONMENT=production
set PYTHONOPTIMIZE=2

echo.
echo 🚀 Starting Blood Report AI Server...
echo.
echo    Dashboard:   http://localhost:8000/
echo    API Docs:    http://localhost:8000/docs
echo    Press CTRL+C to stop
echo.

REM Start instantly
python run_instant.py

pause
