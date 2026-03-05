@echo off
REM Blood Report AI - Death Simple Deployment Launcher
REM Windows Batch - Opens deployment sites automatically

cls
echo.
echo ================================================================================
echo                   BLOOD REPORT AI - QUICK DEPLOY
echo ================================================================================
echo.
echo Your app is ready! Choose ONE deployment method:
echo.
echo   1. 🚂 RAILWAY (Best - https://railway.app)
echo   2. ☁️  VERCEL (Easy - https://vercel.com)
echo   3. 🎨 RENDER (Alternative - https://render.com)
echo   4. 📖 GITHUB (See all guides - https://github.com/loghithakshan/INBLOODO-AGENT26)
echo   5. 🐍 PYTHON GUIDE (Automated setup)
echo.
set /p choice="Enter number (1-5) and press Enter: "

if "%choice%"=="1" (
    echo.
    echo ✅ Opening Railway...
    start https://railway.app/login
    echo.
    echo Steps:
    echo   1. Sign up with GitHub (takes 1 minute)
    echo   2. Click "New Project" ^> "Deploy from GitHub"  
    echo   3. Select: loghithakshan/INBLOODO-AGENT26
    echo   4. Wait 3-5 minutes
    echo   5. Get your live URL!
    echo.
)

if "%choice%"=="2" (
    echo.
    echo ✅ Opening Vercel...
    start https://vercel.com/login
    echo.
    echo Steps:
    echo   1. Sign up with GitHub
    echo   2. Click "Import Project"
    echo   3. URL: https://github.com/loghithakshan/INBLOODO-AGENT26
    echo   4. Click Deploy
    echo   5. Done! (Auto-deploys)
    echo.
)

if "%choice%"=="3" (
    echo.
    echo ✅ Opening Render...
    start https://render.com/
    echo.
    echo Steps:
    echo   1. Sign up with GitHub
    echo   2. "New" ^> "Web Service"
    echo   3. Connect: loghithakshan/INBLOODO-AGENT26
    echo   4. Deploy
    echo.
)

if "%choice%"=="4" (
    echo.
    echo ✅ Opening GitHub repo...
    start https://github.com/loghithakshan/INBLOODO-AGENT26
    echo.
    echo All deployment guides are in the repository!
    echo.
)

if "%choice%"=="5" (
    echo.
    echo Running interactive Railway setup...
    echo.
    cd /d "%~dp0"
    python railway_deploy.py
    if %errorlevel% equ 0 (
        echo.
        echo ✅ DEPLOYMENT SUCCESSFUL!
    ) else (
        echo.
        echo ⚠️  Setup incomplete. Try manual deployment:
        echo    https://railway.app
    )
    echo.
)

echo ================================================================================
echo Press any key to close...
pause >nul
