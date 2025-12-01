@echo off
REM KONTROLLZENTRUM - LAUNCH SCRIPT
REM Python Backend + Windows Desktop App

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 KONTROLLZENTRUM LAUNCHER                              ║
echo ║  Python Backend + Windows Desktop App                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo Wähle Startmodus:
echo.
echo   1. Python Backend (Alle Module)
echo   2. Streamlit Dashboard
echo   3. FastAPI Server
echo   4. Team-Modus (Installation + Ausführung)
echo   5. Roboter-Modus (Interaktiv)
echo   6. Desktop App Setup
echo   7. Alle starten (Parallel)
echo   0. Beenden
echo.

set /p choice="Eingabe (0-7): "

if "%choice%"=="1" (
    echo.
    echo [INFO] Starte Python Backend...
    C:\Python313\python.exe main.py alle run
    pause
) else if "%choice%"=="2" (
    echo.
    echo [INFO] Starte Streamlit Dashboard...
    echo [INFO] Öffnet: http://localhost:8501
    C:\Python313\python.exe -m streamlit run main.py
) else if "%choice%"=="3" (
    echo.
    echo [INFO] Starte FastAPI Server...
    echo [INFO] Öffnet: http://localhost:8003/docs
    C:\Python313\python.exe modules\ki_sideboard.py
) else if "%choice%"=="4" (
    echo.
    echo [INFO] Starte Team-Modus...
    C:\Python313\python.exe main.py team
    pause
) else if "%choice%"=="5" (
    echo.
    echo [INFO] Starte Roboter-Modus...
    C:\Python313\python.exe mega_roboter_ki.py
) else if "%choice%"=="6" (
    echo.
    echo [INFO] Desktop App Setup...
    if not exist "KontrollzentrumApp" mkdir KontrollzentrumApp
    copy KontrollzentrumDesktop.csproj KontrollzentrumApp\ >nul
    copy MainWindow.xaml KontrollzentrumApp\ >nul
    copy MainWindow.xaml.cs KontrollzentrumApp\ >nul
    copy App.xaml KontrollzentrumApp\ >nul
    copy App.xaml.cs KontrollzentrumApp\ >nul
    echo [OK] Dateien kopiert
    echo.
    echo Nächste Schritte:
    echo   cd KontrollzentrumApp
    echo   dotnet run
    pause
) else if "%choice%"=="7" (
    echo.
    echo [INFO] Starte alle Komponenten...
    echo.
    echo [1/3] Python Backend...
    start "Python Backend" C:\Python313\python.exe main.py alle run
    timeout /t 3 /nobreak
    echo.
    echo [2/3] Streamlit Dashboard...
    start "Streamlit Dashboard" C:\Python313\python.exe -m streamlit run main.py
    timeout /t 3 /nobreak
    echo.
    echo [3/3] Desktop App Setup...
    if not exist "KontrollzentrumApp" mkdir KontrollzentrumApp
    copy KontrollzentrumDesktop.csproj KontrollzentrumApp\ >nul
    copy MainWindow.xaml KontrollzentrumApp\ >nul
    copy MainWindow.xaml.cs KontrollzentrumApp\ >nul
    copy App.xaml KontrollzentrumApp\ >nul
    copy App.xaml.cs KontrollzentrumApp\ >nul
    echo [OK] Desktop App bereit
    echo.
    echo Alle Komponenten gestartet!
    pause
) else if "%choice%"=="0" (
    echo [OK] Auf Wiedersehen!
    exit /b 0
) else (
    echo [ERROR] Ungültige Eingabe!
    pause
    goto start
)

pause
