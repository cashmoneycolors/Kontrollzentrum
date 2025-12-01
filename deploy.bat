@echo off
REM Kontrollzentrum - Production Deployment Script

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  KONTROLLZENTRUM - PRODUCTION DEPLOYMENT                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM 1. Prüfe Python
echo [1/5] Prüfe Python-Installation...
C:\Python313\python.exe --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden!
    pause
    exit /b 1
)
echo [OK] Python 3.13 gefunden

REM 2. Installiere Dependencies
echo.
echo [2/5] Installiere Dependencies...
C:\Python313\python.exe -m pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Dependencies-Installation fehlgeschlagen!
    pause
    exit /b 1
)
echo [OK] Dependencies installiert

REM 3. Prüfe API-Keys
echo.
echo [3/5] Prüfe API-Keys...
C:\Python313\python.exe -c "from core.key_check import check_all_keys; check_all_keys()" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Nicht alle API-Keys vorhanden!
    echo [INFO] Bitte .env mit produktiven Keys aktualisieren
    echo.
    pause
)
echo [OK] API-Keys validiert

REM 4. Führe Tests aus
echo.
echo [4/5] Führe Tests aus...
C:\Python313\python.exe -m unittest discover -s tests -p "test_*.py" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Tests fehlgeschlagen!
    pause
    exit /b 1
)
echo [OK] Alle Tests bestanden

REM 5. Starte Anwendung
echo.
echo [5/5] Starte Anwendung...
echo.
echo Wähle Startmodus:
echo   1. CLI-Modus (Alle Module)
echo   2. Streamlit-Dashboard
echo   3. FastAPI-Server
echo   4. Roboter-Modus
echo.
set /p choice="Eingabe (1-4): "

if "%choice%"=="1" (
    echo [INFO] Starte CLI-Modus...
    C:\Python313\python.exe main.py alle run
) else if "%choice%"=="2" (
    echo [INFO] Starte Streamlit-Dashboard...
    C:\Python313\python.exe -m streamlit run main.py
) else if "%choice%"=="3" (
    echo [INFO] Starte FastAPI-Server...
    C:\Python313\python.exe modules\ki_sideboard.py
) else if "%choice%"=="4" (
    echo [INFO] Starte Roboter-Modus...
    C:\Python313\python.exe mega_roboter_ki.py
) else (
    echo [ERROR] Ungültige Eingabe!
    pause
    exit /b 1
)

pause
