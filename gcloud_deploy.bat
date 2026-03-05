@echo off
REM Blood Report AI - Google Cloud Run Deployment Quick Start

echo.
echo ============================================================================
echo   GOOGLE CLOUD RUN - QUICK START DEPLOYMENT
echo ============================================================================
echo.
echo Your Blood Report AI is ready to deploy to Google Cloud Run!
echo.
echo Best for:
echo   - Free tier (2 million requests per month)
echo   - Auto-scaling (0 to 1000+ instances)
echo   - Pay only for what you use
echo   - World-class monitoring
echo.
echo Estimated time: 15 minutes
echo Cost: FREE or $10-20/month for 24/7
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found
    pause
    exit /b 1
)

REM Run deployment guide
python gcloud_deploy.py

echo.
echo ============================================================================
echo   DEPLOYMENT GUIDE COMPLETE
echo ============================================================================
echo.
echo Next: Follow the steps above to deploy to Google Cloud Run
echo.
echo Full documentation: GOOGLE_CLOUD_RUN_GUIDE.md
echo Cloud Console: https://console.cloud.google.com
echo.
pause
