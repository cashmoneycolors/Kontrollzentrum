@echo off
REM Kontrollzentrum - Start App
REM Lädt und startet die App auf dem Laptop

echo.
echo ================================================================================
echo                    KONTROLLZENTRUM - START APP
echo ================================================================================
echo.

REM 1. Python prüfen
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python nicht gefunden!
    echo Bitte Python installieren: https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python gefunden
echo.

REM 2. Requirements installieren
echo [INFO] Installiere Dependencies...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [WARN] Fehler beim Installieren von Dependencies
) else (
    echo [OK] Dependencies installiert
)
echo.

REM 3. Starte App
echo ================================================================================
echo                    STARTE KONTROLLZENTRUM
echo ================================================================================
echo.

python PRODUCTION_GO_LIVE.py

pause
