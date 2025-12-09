@echo off
REM 🚀 BUILD ROBOTER_KI_APP.exe

echo.
echo ========================================
echo 🚀 BUILDING ROBOTER_KI_APP.exe
echo ========================================
echo.

REM Install PyInstaller
echo [1/3] Installing PyInstaller...
pip install pyinstaller -q

REM Build EXE
echo [2/3] Building EXE...
pyinstaller --onefile --windowed --name=ROBOTER_KI_APP --distpath=dist --buildpath=build main.py

REM Copy to Desktop
echo [3/3] Copying to Desktop...
copy dist\ROBOTER_KI_APP.exe "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe"

echo.
echo ========================================
echo ✅ ROBOTER_KI_APP.exe ERSTELLT!
echo ========================================
echo.
echo 📍 Pfad: %USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe
echo.
pause
