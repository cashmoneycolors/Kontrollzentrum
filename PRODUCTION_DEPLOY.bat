@echo off
REM ============================================
REM KONTROLLZENTRUM v5.0 - PRODUCTION DEPLOY
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ============================================
echo 🚀 KONTROLLZENTRUM - PRODUCTION DEPLOYMENT
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nicht gefunden!
    echo Installiere Python 3.9+ von https://python.org
    pause
    exit /b 1
)
echo ✅ Python gefunden

REM Check .env
if not exist .env (
    echo ⚠️  .env nicht gefunden - erstelle mit Defaults
    (
        echo ENVIRONMENT=production
        echo DEBUG=false
        echo LOG_LEVEL=INFO
    ) > .env
    echo ✅ .env erstellt
) else (
    echo ✅ .env vorhanden
)

REM Install dependencies
echo.
echo 🔄 Installiere Dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ⚠️  Einige Dependencies konnten nicht installiert werden
) else (
    echo ✅ Dependencies installiert
)

REM Create database
echo.
echo 🔄 Initialisiere Database...
python -c "from core.database import db; db.create_all()" 2>nul
if errorlevel 0 (
    echo ✅ Database initialisiert
)

REM Show menu
echo.
echo ============================================
echo 🎛️  PRODUCTION MENU
echo ============================================
echo 1. 🚀 Team-Modus (alle Module)
echo 2. 🌐 API Gateway
echo 3. 🏥 Health Check
echo 4. 📊 Dashboard (Streamlit)
echo 5. 🔧 CLI Mode
echo 6. ❌ Beenden
echo ============================================
echo.

set /p choice="Wähle Option (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🔄 Starte Team-Modus...
    python main.py team
) else if "%choice%"=="2" (
    echo.
    echo 🔄 Starte API Gateway...
    python main.py api
) else if "%choice%"=="3" (
    echo.
    echo 🔄 Starte Health Check...
    python main.py health
) else if "%choice%"=="4" (
    echo.
    echo 🔄 Starte Streamlit Dashboard...
    streamlit run main.py
) else if "%choice%"=="5" (
    echo.
    echo 🔄 Starte CLI Mode...
    python main.py
) else if "%choice%"=="6" (
    echo.
    echo 👋 Auf Wiedersehen!
    exit /b 0
) else (
    echo ❌ Ungültige Option
    pause
    exit /b 1
)

pause
