# 🤖 ROBOTER_KI_APP - PowerShell Launcher

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                            ║" -ForegroundColor Cyan
    Write-Host "║          🤖 ROBOTER KI APP v5.0                          ║" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[1] 🚀 Start Team Mode" -ForegroundColor Yellow
    Write-Host "[2] 🔌 Start API Gateway" -ForegroundColor Yellow
    Write-Host "[3] 📊 Start Dashboard" -ForegroundColor Yellow
    Write-Host "[4] 🏥 Health Check" -ForegroundColor Yellow
    Write-Host "[5] 📋 Run Week 1 - GitHub Integration" -ForegroundColor Yellow
    Write-Host "[6] 📋 Run Week 2 - Production Build" -ForegroundColor Yellow
    Write-Host "[7] 📋 Run Week 3 - Deployment" -ForegroundColor Yellow
    Write-Host "[8] 📋 Run Week 4 - Monetization" -ForegroundColor Yellow
    Write-Host "[9] 🚀 Run All Weeks" -ForegroundColor Yellow
    Write-Host "[0] ❌ Exit" -ForegroundColor Red
    Write-Host ""
}

do {
    Show-Menu
    $choice = Read-Host "Select option"
    
    switch ($choice) {
        "1" { python main.py team }
        "2" { python main.py api }
        "3" { streamlit run main.py }
        "4" { python main.py health }
        "5" { python WEEK_1_EXECUTION.py }
        "6" { python WEEK_2_EXECUTION.py }
        "7" { python WEEK_3_EXECUTION.py }
        "8" { python WEEK_4_EXECUTION.py }
        "9" { python RUN_NOW.py }
        "0" { exit }
    }
    
    Read-Host "Press Enter to continue"
} while ($true)
