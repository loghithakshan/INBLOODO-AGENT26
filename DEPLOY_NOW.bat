@echo off
REM Blood Report AI - Deploy Now Script
REM Open deployment platforms and show instructions

cls
color 0A
echo.
echo ================================================================================
echo.
echo                  🎉 BLOOD REPORT AI - READY TO DEPLOY! 🎉
echo.
echo ================================================================================
echo.
echo Your app is PRODUCTION-READY. Choose what to do:
echo.
echo   [1] Deploy to VERCEL (Fastest - 2 minutes)
echo   [2] Deploy to RAILWAY (Recommended - 3 minutes) 
echo   [3] Deploy to RENDER (Alternative - 3 minutes)
echo   [4] Setup GITHUB ACTIONS (Auto-deploy - 5 min, then fully auto)
echo   [5] View deployment guides (All info in one doc)
echo   [6] Open GitHub repo
echo   [7] View GitHub Actions status
echo   [8] Exit
echo.
set /p choice="Choose (1-8): "

if "%choice%"=="1" (
  cls
  color 0B
  echo.
  echo 🌐 Opening Vercel...
  echo.
  echo Steps:
  echo   1. Open: https://vercel.com/import
  echo   2. Click "GitHub" button
  echo   3. Authorize GitHub
  echo   4. Select: loghithakshan/INBLOODO-AGENT26
  echo   5. Click "Import"
  echo   Done! Auto-deploys on every push.
  echo.
  start https://vercel.com/import
  timeout /t 3 /nobreak
  exit /b 0
)

if "%choice%"=="2" (
  cls
  color 09
  echo.
  echo 🚂 Opening Railway...
  echo.
  echo Steps:
  echo   1. Open: https://railway.app
  echo   2. Sign up with GitHub
  echo   3. Click "New Project"
  echo   4. Click "Deploy from GitHub"  
  echo   5. Select: loghithakshan/INBLOODO-AGENT26
  echo   6. Wait 3-5 minutes
  echo   Done! You'll get a live URL.
  echo.
  start https://railway.app
  timeout /t 3 /nobreak
  exit /b 0
)

if "%choice%"=="3" (
  cls
  color 05
  echo.
  echo 🎨 Opening Render...
  echo.
  echo Steps:
  echo   1. Open: https://render.com
  echo   2. Sign up with GitHub
  echo   3. Click "New" then "Web Service"
  echo   4. Select: loghithakshan/INBLOODO-AGENT26
  echo   5. Click "Create Web Service"
  echo   6. Wait 2-3 minutes
  echo   Done! You'll get a live URL.
  echo.
  start https://render.com
  timeout /t 3 /nobreak
  exit /b 0
)

if "%choice%"=="4" (
  cls
  color 06
  echo.
  echo 🤖 Setting up GitHub Actions Auto-Deploy...
  echo.
  echo   1. Get Railway token: https://railway.app/account/tokens
  echo   2. Click "Create Token"
  echo   3. Copy it
  echo   4. Go to GitHub Secrets: https://github.com/loghithakshan/INBLOODO-AGENT26/settings/secrets/actions
  echo   5. Click "New repository secret"
  echo   6. Name: RAILWAY_TOKEN
  echo   7. Paste your token
  echo   8. Click "Add secret"
  echo.
  echo   Then run:
  echo   git push origin main
  echo.
  echo   And watch: https://github.com/loghithakshan/INBLOODO-AGENT26/actions
  echo.
  start https://railway.app/account/tokens
  timeout /t 3 /nobreak
  start https://github.com/loghithakshan/INBLOODO-AGENT26/settings/secrets/actions
  timeout /t 3 /nobreak
  exit /b 0
)

if "%choice%"=="5" (
  cls
  color 0E
  echo.
  echo 📖 Opening deployment guides...
  echo.
  start https://github.com/loghithakshan/INBLOODO-AGENT26
  timeout /t 2 /nobreak
  echo.
  echo Key files to read:
  echo   - START_DEPLOYMENT_NOW.md (quickest guide)
  echo   - GITHUB_ACTIONS_AUTO_DEPLOY.md (auto-deploy)
  echo   - DEPLOYMENT_PLATFORMS_GUIDE.md (comparison)
  echo   - RAILWAY_DEPLOYMENT_GUIDE.md (detailed)
  echo.
  timeout /t 5 /nobreak
  exit /b 0
)

if "%choice%"=="6" (
  cls
  color 0B
  echo.
  echo Opening GitHub repository...
  echo.
  start https://github.com/loghithakshan/INBLOODO-AGENT26
  timeout /t 2 /nobreak
  exit /b 0
)

if "%choice%"=="7" (
  cls
  color 0A
  echo.
  echo Opening GitHub Actions...
  echo.
  start https://github.com/loghithakshan/INBLOODO-AGENT26/actions
  timeout /t 2 /nobreak
  exit /b 0
)

echo.
echo Exiting...
timeout /t 1 /nobreak
