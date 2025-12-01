@echo off
REM ============================================
REM KONTROLLZENTRUM - PRODUCTION LAUNCHER
REM ============================================

setlocal enabledelayedexpansion

echo.
echo 🚀 KONTROLLZENTRUM - PRODUCTION GRADE
echo ============================================
echo.

:menu
echo.
echo 📋 SELECT MODE:
echo.
echo   1) 🌐 API Gateway (Port 8000)
echo   2) 📊 Health Check
echo   3) 🏃 Team Mode (All Modules)
echo   4) 🎯 CLI Mode
echo   5) 📈 Dashboard (Streamlit)
echo   6) 🔐 Generate Auth Tokens
echo   7) 📊 View Metrics
echo   8) ❌ Exit
echo.

set /p choice="Enter choice (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🌐 Starting API Gateway...
    python main.py api
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 📊 Running Health Checks...
    python main.py health
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 🏃 Running Team Mode...
    python main.py team
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 🎯 Starting CLI Mode...
    python main.py
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 📈 Starting Dashboard...
    streamlit run main.py
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo 🔐 Generating Auth Tokens...
    python core/auth.py
    pause
    goto menu
)

if "%choice%"=="7" (
    echo.
    echo 📊 Viewing Metrics...
    python -c "from core.database import db; import json; logs = db.get_results(limit=10); print(json.dumps(logs, indent=2))"
    pause
    goto menu
)

if "%choice%"=="8" (
    echo.
    echo ✅ Goodbye!
    exit /b 0
)

echo Invalid choice. Please try again.
goto menu
