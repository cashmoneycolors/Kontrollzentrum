@echo off
REM 🤖 ROBOTER_KI_APP - Standalone Batch Launcher

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║          🤖 ROBOTER KI APP v5.0                          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [1] 🚀 Start Team Mode
echo [2] 🔌 Start API Gateway
echo [3] 📊 Start Dashboard
echo [4] 🏥 Health Check
echo [5] 📋 Run Week 1 - GitHub Integration
echo [6] 📋 Run Week 2 - Production Build
echo [7] 📋 Run Week 3 - Deployment
echo [8] 📋 Run Week 4 - Monetization
echo [9] 🚀 Run All Weeks
echo [0] ❌ Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto team_mode
if "%choice%"=="2" goto api_gateway
if "%choice%"=="3" goto dashboard
if "%choice%"=="4" goto health_check
if "%choice%"=="5" goto week1
if "%choice%"=="6" goto week2
if "%choice%"=="7" goto week3
if "%choice%"=="8" goto week4
if "%choice%"=="9" goto all_weeks
if "%choice%"=="0" exit /b

goto menu

:team_mode
python main.py team
pause
goto menu

:api_gateway
python main.py api
pause
goto menu

:dashboard
streamlit run main.py
pause
goto menu

:health_check
python main.py health
pause
goto menu

:week1
python WEEK_1_EXECUTION.py
pause
goto menu

:week2
python WEEK_2_EXECUTION.py
pause
goto menu

:week3
python WEEK_3_EXECUTION.py
pause
goto menu

:week4
python WEEK_4_EXECUTION.py
pause
goto menu

:all_weeks
python RUN_NOW.py
pause
goto menu
