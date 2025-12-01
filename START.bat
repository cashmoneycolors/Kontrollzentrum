@echo off
REM Kontrollzentrum - START Script

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 KONTROLLZENTRUM - START                               ║
echo ║  Python Backend + Windows Desktop App                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/3] Starte Python Backend...
echo.
C:\Python313\python.exe main.py alle run
echo.

echo [2/3] Team-Modus...
echo.
C:\Python313\python.exe main.py team
echo.

echo [3/3] Desktop App Setup...
echo.
echo Öffne Terminal und führe aus:
echo   cd KontrollzentrumApp
echo   dotnet run
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✅ PROJEKT GESTARTET                                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
