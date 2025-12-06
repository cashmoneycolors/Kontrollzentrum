@echo off
REM Gebe Ausführungsrechte für Python-Skripte frei

echo Gebe Ausführungsrechte frei...

REM Ändere Berechtigungen für das Verzeichnis
icacls "c:\Users\Laptop\Kontrollzentrum-1" /grant:r "%USERNAME%:F" /T /C

echo.
echo ✅ Berechtigungen aktualisiert!
echo.
echo Starte jetzt: START.bat
echo.
pause
