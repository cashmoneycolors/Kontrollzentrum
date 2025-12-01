@echo off
REM ============================================
REM KONTROLLZENTRUM - GITHUB SETUP
REM ============================================

setlocal enabledelayedexpansion

echo.
echo 🚀 KONTROLLZENTRUM - GITHUB SETUP
echo ============================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

REM Initialize git repository
echo 📝 Initializing Git repository...
git init
git config user.name "Kontrollzentrum Developer"
git config user.email "dev@kontrollzentrum.local"

echo.
echo 📋 Git Configuration:
git config --list | findstr "user"

echo.
echo 📁 Adding files to git...
git add .

echo.
echo 📊 Status:
git status

echo.
echo ============================================
echo ✅ NEXT STEPS:
echo ============================================
echo.
echo 1. Create repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Copy the repository URL
echo.
echo 3. Run these commands:
echo    git remote add origin https://github.com/YOUR_USERNAME/Kontrollzentrum.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Verify on GitHub:
echo    https://github.com/YOUR_USERNAME/Kontrollzentrum
echo.
echo ============================================
echo.

pause
