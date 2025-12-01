@echo off
REM ============================================
REM KONTROLLZENTRUM - GIT PUSH AUTOMATION
REM ============================================

setlocal enabledelayedexpansion

echo.
echo 📤 KONTROLLZENTRUM - GIT PUSH
echo ============================================
echo.

REM Check if git is initialized
if not exist .git (
    echo ❌ Git repository not initialized!
    echo Run: GITHUB_SETUP.bat
    pause
    exit /b 1
)

REM Get commit message
set /p message="Enter commit message: "

if "!message!"=="" (
    echo ❌ Commit message cannot be empty!
    exit /b 1
)

echo.
echo 📝 Staging files...
git add .

echo.
echo 📊 Status:
git status

echo.
echo 💾 Committing...
git commit -m "!message!"

if errorlevel 1 (
    echo ⚠️  Nothing to commit or error occurred
    pause
    exit /b 1
)

echo.
echo 📤 Pushing to GitHub...
git push

if errorlevel 1 (
    echo ❌ Push failed!
    echo Make sure you have:
    echo   1. Created repository on GitHub
    echo   2. Added remote: git remote add origin https://github.com/YOUR_USERNAME/Kontrollzentrum.git
    echo   3. Set up authentication
    pause
    exit /b 1
)

echo.
echo ✅ Push successful!
echo.
echo 🔗 View on GitHub:
git remote -v | findstr "origin"
echo.

pause
