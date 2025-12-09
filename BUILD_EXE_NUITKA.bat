@echo off
REM 🚀 BUILD ROBOTER_KI_APP.exe - NUITKA METHOD (FASTEST)

echo.
echo ========================================
echo 🚀 BUILDING ROBOTER_KI_APP.exe
echo ========================================
echo.

REM Install Nuitka
echo [1/3] Installing Nuitka...
pip install nuitka -q

REM Build EXE
echo [2/3] Building EXE with Nuitka...
python -m nuitka --onefile --windows-disable-console --output-dir=dist roboter_ki_gui.py

REM Copy to Desktop
echo [3/3] Copying to Desktop...
if not exist "%USERPROFILE%\Desktop\Projekte" mkdir "%USERPROFILE%\Desktop\Projekte"
copy dist\roboter_ki_gui.exe "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe"

echo.
echo ========================================
echo ✅ ROBOTER_KI_APP.exe ERSTELLT!
echo ========================================
echo.
echo 📍 Pfad: %USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe
echo.
pause
