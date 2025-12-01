param(
    [string]$Target = 'C:\Users\Laptop\Desktop\Projekte\MEGA ULTRA ROBOTER KI',
    [string]$Python = 'C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.2544.0_x64__qbz5n2kfra8p0\python3.13.exe',
    [switch]$Verbose
)

$ErrorActionPreference = 'Continue'

if (!(Test-Path $Python)) {
    Write-Error "Python interpreter not found: $Python"
    exit 2
}

if (!(Test-Path $Target)) {
    Write-Error "Target path not found: $Target"
    exit 3
}

Write-Host "Using Python interpreter: $Python"
Write-Host "Scanning target: $Target"

# Collect Python files excluding __pycache__ directories
$files = Get-ChildItem -Path $Target -Recurse -Include *.py -File -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '__pycache__' }

if ($files.Count -eq 0) {
    Write-Warning "No .py files found under $Target"
}

$errors = @()
$ok = 0

foreach ($file in $files) {
    try {
        & "$Python" -m py_compile "$($file.FullName)" 2>$null
        $ok++
        if ($Verbose) { Write-Host "[OK] $($file.FullName)" }
    }
    catch {
        $err = $_.Exception.Message
        $errors += [PSCustomObject]@{ File=$file.FullName; Error=$err }
        Write-Host "[FAIL] $($file.FullName)" -ForegroundColor Red
    }
}

$reportPath = Join-Path $PWD 'SYNTAX_ERRORS_REPORT.txt'
"SYNTAX SCAN REPORT $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File $reportPath -Encoding UTF8
"TARGET: $Target" | Add-Content $reportPath
"PYTHON: $Python" | Add-Content $reportPath
"TOTAL FILES: $($files.Count)" | Add-Content $reportPath
"SUCCESS: $ok" | Add-Content $reportPath
"FAILURES: $($errors.Count)" | Add-Content $reportPath
Add-Content $reportPath ""

if ($errors.Count -gt 0) {
    foreach ($e in $errors) {
        "FILE: $($e.File)" | Add-Content $reportPath
        "ERROR: $($e.Error)" | Add-Content $reportPath
        Add-Content $reportPath ""
    }
    Write-Host "Syntax errors found: $($errors.Count). See $reportPath" -ForegroundColor Yellow
    exit 1
} else {
    Add-Content $reportPath "ALL OK - No syntax errors detected"
    Write-Host "All Python files compiled successfully. Report: $reportPath" -ForegroundColor Green
    exit 0
}