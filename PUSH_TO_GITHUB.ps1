# 🚀 PUSH TO GITHUB - PowerShell Version

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 KONTROLLZENTRUM - GITHUB PUSH" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Schritt 1: GitHub Token
Write-Host "[1/4] GitHub Token erforderlich" -ForegroundColor Yellow
Write-Host "Gehe zu: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "Erstelle einen 'Personal Access Token' mit 'repo' Berechtigung" -ForegroundColor Gray
Write-Host ""
$GITHUB_TOKEN = Read-Host "Gib deinen GitHub Token ein"

# Schritt 2: Username
Write-Host ""
$GITHUB_USER = Read-Host "Gib deinen GitHub Username ein"

# Schritt 3: Repository Name
Write-Host ""
$REPO_NAME = Read-Host "Repository Name (default: kontrollzentrum)"
if ([string]::IsNullOrEmpty($REPO_NAME)) { $REPO_NAME = "kontrollzentrum" }

# Schritt 4: Remote URL
Write-Host ""
Write-Host "[2/4] Setze Remote URL..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin "https://$($GITHUB_TOKEN)@github.com/$($GITHUB_USER)/$($REPO_NAME).git"

# Schritt 5: Branch
Write-Host "[3/4] Richte main Branch ein..." -ForegroundColor Yellow
git branch -M main

# Schritt 6: Push
Write-Host "[4/4] Pushe zu GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ ERFOLGREICH ZU GITHUB GEPUSHT!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Repository: https://github.com/$($GITHUB_USER)/$($REPO_NAME)" -ForegroundColor Green
Write-Host ""
