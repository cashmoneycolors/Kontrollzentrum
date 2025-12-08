@echo off
REM 🚀 PUSH TO GITHUB SCRIPT

echo.
echo ========================================
echo 🚀 KONTROLLZENTRUM - GITHUB PUSH
echo ========================================
echo.

REM Schritt 1: GitHub Token eingeben
echo [1/4] GitHub Token erforderlich
echo Gehe zu: https://github.com/settings/tokens
echo Erstelle einen "Personal Access Token" mit "repo" Berechtigung
echo.
set /p GITHUB_TOKEN="Gib deinen GitHub Token ein: "

REM Schritt 2: Username eingeben
echo.
set /p GITHUB_USER="Gib deinen GitHub Username ein: "

REM Schritt 3: Repository Name
echo.
set /p REPO_NAME="Repository Name (default: kontrollzentrum): "
if "%REPO_NAME%"=="" set REPO_NAME=kontrollzentrum

REM Schritt 4: Remote URL setzen
echo.
echo [2/4] Setze Remote URL...
git remote remove origin 2>nul
git remote add origin https://%GITHUB_TOKEN%@github.com/%GITHUB_USER%/%REPO_NAME%.git

REM Schritt 5: Branch umbenennen
echo [3/4] Richte main Branch ein...
git branch -M main

REM Schritt 6: Push
echo [4/4] Pushe zu GitHub...
git push -u origin main

echo.
echo ========================================
echo ✅ ERFOLGREICH ZU GITHUB GEPUSHT!
echo ========================================
echo.
echo 📍 Repository: https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
pause
