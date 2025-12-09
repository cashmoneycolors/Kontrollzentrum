@echo off
REM 🚀 BUILD ROBOTER_KI_APP.exe - DIRECT METHOD

echo.
echo ========================================
echo 🚀 BUILDING ROBOTER_KI_APP.exe
echo ========================================
echo.

REM Install cx_Freeze
echo [1/4] Installing cx_Freeze...
pip install cx_Freeze -q

REM Create setup.py
echo [2/4] Creating setup.py...
(
echo from cx_Freeze import setup, Executable
echo setup(
echo     name="ROBOTER_KI_APP",
echo     version="5.0",
echo     description="Kontrollzentrum v5.0",
echo     executables=[Executable("roboter_ki_gui.py", base="Win32GUI")]
echo ^)
) > setup.py

REM Build EXE
echo [3/4] Building EXE...
python setup.py build

REM Copy to Desktop
echo [4/4] Copying to Desktop...
if not exist "%USERPROFILE%\Desktop\Projekte" mkdir "%USERPROFILE%\Desktop\Projekte"
copy build\exe.win-amd64-3.11\ROBOTER_KI_APP.exe "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe"

echo.
echo ========================================
echo ✅ ROBOTER_KI_APP.exe ERSTELLT!
echo ========================================
echo.
echo 📍 Pfad: %USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.exe
echo.
pause
