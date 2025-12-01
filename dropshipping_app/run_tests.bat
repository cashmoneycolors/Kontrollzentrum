@echo off
echo.
echo ========================================
echo  DROPSHIPPING APP - TEST SUITE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo [2/3] Installing dependencies...
pip install -q fastapi uvicorn streamlit requests python-dotenv sqlalchemy pydantic pandas aiohttp
if errorlevel 1 (
    echo WARNING: Some dependencies failed to install
)

echo.
echo [3/3] Running tests...
python test_app.py

echo.
pause
