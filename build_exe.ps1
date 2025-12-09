# 🚀 BUILD ROBOTER_KI_APP.exe - PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 BUILDING ROBOTER_KI_APP.exe" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install PyInstaller
Write-Host "[1/3] Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller -q

# Step 2: Build EXE
Write-Host "[2/3] Building EXE..." -ForegroundColor Yellow
pyinstaller --onefile --windowed --name=ROBOTER_KI_APP --distpath=dist --buildpath=build main.py

# Step 3: Copy to Desktop
Write-Host "[3/3] Copying to Desktop..." -ForegroundColor Yellow
$desktopPath = "$env:USERPROFILE\Desktop\Projekte"
if (-not (Test-Path $desktopPath)) {
    New-Item -ItemType Directory -Path $desktopPath -Force | Out-Null
}
Copy-Item "dist\ROBOTER_KI_APP.exe" "$desktopPath\ROBOTER_KI_APP.exe" -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ ROBOTER_KI_APP.exe ERSTELLT!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Pfad: $desktopPath\ROBOTER_KI_APP.exe" -ForegroundColor Green
Write-Host ""
