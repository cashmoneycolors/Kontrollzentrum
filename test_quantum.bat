@echo off
REM Test Quantum Module in Terminal

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  QUANTUM COMPUTING MODULE TEST                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/3] Teste Quantum Modul direkt...
echo.
C:\Python313\python.exe -c "from modules.quantum_demo_modul import run; import json; result = run(); print(json.dumps(result, indent=2, default=str))"

echo.
echo [2/3] Teste alle 16 Module...
echo.
C:\Python313\python.exe main.py alle run

echo.
echo [3/3] Team-Modus...
echo.
C:\Python313\python.exe main.py team

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST ABGESCHLOSSEN                                       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
