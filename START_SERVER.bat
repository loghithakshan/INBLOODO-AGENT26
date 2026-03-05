@echo off
REM ============================================================================
REM BLOOD REPORT AI - ULTIMATE SERVER LAUNCHER
REM ============================================================================
REM This script handles everything:
REM - Python validation
REM - Virtual environment setup
REM - Dependency installation
REM - Server startup
REM - Automatic browser opening
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo          BLOOD REPORT AI - INTELLIGENT SERVER LAUNCHER v2.0
echo ============================================================================
echo.
echo  This script will automatically:
echo  1. Check Python installation
echo  2. Create/update virtual environment
echo  3. Install all dependencies
echo  4. Start the AI server
echo  5. Open your browser to the dashboard
echo.
echo ============================================================================
echo.

REM STEP 1: Check Python
echo [STEP 1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ^^!ERROR: Python not found!
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo  ✓ %PYTHON_VERSION% found
echo.

REM STEP 2: Create/Check Virtual Environment
echo [STEP 2/6] Setting up Python virtual environment...
if not exist "venv\" (
    echo  Creating new venv (this may take a moment)...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo  ^^!ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo  ✓ Virtual environment created
) else (
    echo  ✓ Virtual environment exists
)
echo.

REM STEP 3: Activate Virtual Environment
echo [STEP 3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo  ^^!ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo  ✓ Virtual environment activated
echo.

REM STEP 4: Install Dependencies
echo [STEP 4/6] Installing dependencies...
echo  (This may take 2-3 minutes on first run)
echo.
pip install -r requirements.txt --upgrade --quiet
if %errorlevel% neq 0 (
    echo  WARNING: Some dependencies had issues, but continuing...
)
echo  ✓ Dependencies installed
echo.

REM STEP 5: Verify Setup
echo [STEP 5/6] Verifying installation...
python -c "import fastapi; import uvicorn; print('  ✓ Core libraries OK')"
if %errorlevel% neq 0 (
    echo  ^^!ERROR: Core libraries failed validation
    pause
    exit /b 1
)
echo.

REM STEP 6: Start Server
echo [STEP 6/6] Starting Blood Report AI Server...
echo.
echo ============================================================================
echo          SERVER STARTUP - WATCH FOR SUCCESS MESSAGE BELOW
echo ============================================================================
echo.
echo  Waiting for server initialization...
echo  (This takes 10-15 seconds)
echo.
echo  Accessible at:
echo    Dashboard:     http://localhost:8000/
echo    API Docs:      http://localhost:8000/docs
echo    Health Check:  http://localhost:8000/health
echo.
echo  Press CTRL+C to stop the server
echo.
echo ============================================================================
echo.

REM Start server with enhanced visibility
start "Blood Report AI Server" python main.py

REM Wait for server to start and then open browser
timeout /t 3 /nobreak >nul

REM Try to open browser (Windows 10+)
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if %VERSION% geq 10.0 (
    start http://localhost:8000/
)

echo.
echo ============================================================================
echo                    SERVER IS RUNNING IN NEW WINDOW
echo ============================================================================
echo.
echo If browser didn't open, visit: http://localhost:8000/
echo.
echo To stop the server, close the "Blood Report AI Server" window
echo.
echo ============================================================================
echo.
pause
exit /b 0
