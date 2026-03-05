@echo off
REM Blood Report AI - Quick Deploy Script for Windows

echo.
echo ============================================================
echo   BLOOD REPORT AI - DEPLOYMENT SETUP
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python first.
    pause
    exit /b 1
)

echo Checking prerequisites...
python deploy.py

if %errorlevel% neq 0 (
    echo Error during deployment setup
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   DEPLOYMENT SETUP COMPLETE!
echo ============================================================
echo.
echo Next Steps:
echo 1. Go to https://railway.app
echo 2. Sign in with GitHub
echo 3. Create New Project - Deploy from GitHub
echo 4. Select: loghithakshan/INBLOODO-AGENT26
echo 5. Add your API keys as environment variables
echo 6. Click Deploy
echo.
pause
