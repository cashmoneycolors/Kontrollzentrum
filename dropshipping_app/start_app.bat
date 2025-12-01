@echo off
echo.
echo ========================================
echo  DROPSHIPPING APP - STARTER
echo ========================================
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo Starting API Server on http://localhost:8000
echo.
start cmd /k "python main.py"

timeout /t 3

echo.
echo Starting Dashboard on http://localhost:8501
echo.
start cmd /k "streamlit run dashboard.py"

echo.
echo ✅ App started!
echo    - API: http://localhost:8000
echo    - Dashboard: http://localhost:8501
echo    - Docs: http://localhost:8000/docs
echo.
pause
