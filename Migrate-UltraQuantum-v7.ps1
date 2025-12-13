# ============================================================
# MIGRATE-ULTRAQUANTUM-V7.PS1
# Kontrollzentrum v5.0 - Ultra Quantum Migration Script
# ============================================================

param(
    [switch]$Full,
    [switch]$Test,
    [switch]$Deploy
)

Write-Host "🚀 ULTRA QUANTUM MIGRATION v7.0" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 1. GITHUB INTEGRATION
Write-Host "`n[1/5] GitHub Integration..." -ForegroundColor Yellow
git status
git add .
git commit -m "🔄 Auto-Migration $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push -u origin blackboxai/azure-mcp-setup

# 2. DEPENDENCIES
Write-Host "`n[2/5] Installing Dependencies..." -ForegroundColor Yellow
py -3.11 -m pip install -r requirements.txt

# 3. TESTS
Write-Host "`n[3/5] Running Tests..." -ForegroundColor Yellow
py -3.11 -m pytest tests/ -v

# 4. BUILD
Write-Host "`n[4/5] Building Docker Image..." -ForegroundColor Yellow
docker build -t kontrollzentrum:5.0 .

# 5. DEPLOY
Write-Host "`n[5/5] Deploying..." -ForegroundColor Yellow
if ($Deploy) {
    docker-compose up -d
    Write-Host "✅ Deployed!" -ForegroundColor Green
}

# START SYSTEM
Write-Host "`n🎯 Starting System..." -ForegroundColor Cyan
py -3.11 main.py

Write-Host "`n✅ MIGRATION COMPLETE!" -ForegroundColor Green
Write-Host "💰 Revenue Target: €3.25M Year 1" -ForegroundColor Magenta