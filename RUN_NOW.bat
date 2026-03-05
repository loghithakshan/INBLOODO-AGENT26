@echo off
REM ============================================================================
REM BLOOD REPORT AI - ONE-CLICK SETUP & LAUNCHER (WINDOWS)
REM ============================================================================
REM This is the absolute simplest way to get the server running
REM Just run this file and everything will be set up automatically
REM ============================================================================

setlocal enabledelayedexpansion

color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║     BLOOD REPORT AI - ONE-CLICK SETUP & SERVER LAUNCHER               ║
echo ║                                                                        ║
echo ║     This script will automatically:                                   ║
echo ║     1. Check Python installation                                      ║
echo ║     2. Create virtual environment                                     ║
echo ║     3. Install all dependencies                                       ║
echo ║     4. Start the AI-powered blood report analysis server              ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  ERROR: Python not found!
    echo.
    echo  Please install Python 3.8+ from:
    echo  https://www.python.org/downloads/
    echo.
    echo  During installation, MAKE SURE to check:
    echo  ✓ Add Python to PATH
    echo.
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=*" %%i in ('python --version') do (
    echo  Python Found: %%i
)
echo.

REM Run the ultimate setup script
echo  Starting comprehensive setup and server launch...
echo.

python ultimate_setup.py

REM If we get here, server exited
if %errorlevel% neq 0 (
    echo.
    echo  Server exited with an error.
    echo.
)

pause
exit /b %errorlevel%
