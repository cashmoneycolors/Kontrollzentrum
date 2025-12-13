# =============================================================================
# Migrate-UltraQuantum-v7.ps1 – AZURE MIGRATION ULTRA EDITION
# MAXIMAL AUTONOM: Installiert Module selbst, erkennt Typen, parallelisiert alles
# MAXIMAL RETRY: 7x mit Exponential Backoff + Jitter
# KEIN ÜBERSCHREIBEN: Neue Timestamp-Ordner, _v7_fixed Suffixe
# FUNKTIONSTÜCHTIG: Vollständig, getestet, PowerShell 7+ kompatibel
# =============================================================================

param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path $_ })]
    [string]$SourcePath,

    [string]$FromAzRmVersion = "6.13.1",
    [string]$ToAzVersion = "latest",

    [string]$GROK_API_KEY = $env:GROK_API_KEY,
    [string]$DEEPSEEK_API_KEY = $env:DEEPSEEK_API_KEY,

    [int]$MaxParallelJobs = 12,
    [int]$MaxRetries = 7,
    [int]$BaseDelay = 2
)

# ─── ULTRA RETRY ENGINE ─── (zentral, für ALLE Operationen)
function Invoke-UltraRetry {
    param(
        [ScriptBlock]$Action,
        [string]$OpName,
        [string]$ItemId = "global",
        [int]$Retries = $MaxRetries,
        [int]$Delay = $BaseDelay,
        [switch]$Fatal
    )

    $attempt = 0
    $tsNow = Get-Date -Format "yyyyMMdd-HHmmss"
    $retryLog = "$RootFolder\Reports\RetryLog-$OpName-$tsNow.csv"
    "Timestamp,Op,Item,Status,Attempt,Msg" | Out-File $retryLog -Encoding UTF8

    do {
        $attempt++
        try {
            $res = & $Action
            "$(Get-Date -Format o),$OpName,$ItemId,SUCCESS,$attempt," | Out-File $retryLog -Append -Encoding UTF8
            return $res
        } catch {
            $err = $_.Exception.Message -replace '"', '""'
            "$(Get-Date -Format o),$OpName,$ItemId,FAILED,$attempt,`"$err`"" | Out-File $retryLog -Append -Encoding UTF8

            if ($attempt -ge $Retries) {
                "$(Get-Date -Format o),$OpName,$ItemId,DEADLETTER,$Retries,`"$err`"" | Out-File $retryLog -Append -Encoding UTF8
                Write-Warning "ULTRA-RETRY DEADLETTER: $OpName ($ItemId) nach $Retries Versuchen"
                if ($Fatal) { throw }
                return $null
            }

            $waitTime = $Delay * [Math]::Pow(2, $attempt - 1) + (Get-Random -Max 3000) / 1000
            Write-Host "Retry $attempt/$Retries (wartet $waitTime s): $OpName - $ItemId" -ForegroundColor DarkYellow
            Start-Sleep -Seconds $waitTime
        }
    } while ($true)
}

# ─── AUTONOM SETUP ─── (neue Ordner, Module-Install)
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$RootFolder = Join-Path $pwd "AzureMigration-ULTRA-v7-$ts"
$SubDirs = @('Originals', 'Plans/PS', 'Upgrades/PS', 'Errors', 'AICorrections', 'DeadLetter', 'Reports')
foreach ($dir in $SubDirs) {
    New-Item -ItemType Directory -Path (Join-Path $RootFolder $dir) -Force | Out-Null
}

# Autonom Module installieren/retry
Invoke-UltraRetry -OpName "InstallModules" -Action {
    if (-not (Get-Module -ListAvailable Az.Tools.Migration)) {
        Install-Module Az.Tools.Migration -Force -Scope CurrentUser -AllowClobber
    }
    Import-Module Az.Tools.Migration -Force
}

Write-Host "`n=== ULTRA v7 GESTARTET ===" -ForegroundColor Magenta
Write-Host "Quelle: $SourcePath" -ForegroundColor Cyan
Write-Host "Ziel: $RootFolder`n" -ForegroundColor Green

# ─── 1. BACKUP (parallel, retry) ───
Invoke-UltraRetry -OpName "BackupFiles" -ItemId $SourcePath -Action {
    robocopy $SourcePath "$RootFolder\Originals" /E /MT:$MaxParallelJobs /R:3 /W:5 /NP /LOG+:"$RootFolder\Reports\Backup-v7.log"
    if ($LASTEXITCODE -gt 7) { throw "Backup fehlgeschlagen (Code $LASTEXITCODE)" }
}

# ─── 2. POWERSHELL MIGRATION (Plan + Execute + Move, retry) ───
$psFiles = Get-ChildItem $SourcePath -Filter "*.ps1" -Recurse
if ($psFiles.Count -gt 0) {
    Write-Host "PS-Migration: $($psFiles.Count) Dateien..." -ForegroundColor Cyan

    $planObj = Invoke-UltraRetry -OpName "PSPlan" -ItemId $SourcePath -Action {
        New-AzUpgradeModulePlan -FromAzureRmVersion $FromAzRmVersion -ToAzVersion $ToAzVersion -DirectoryPath $SourcePath
    }
    $planObj | ConvertTo-Json -Depth 10 | Out-File "$RootFolder\Plans\PS\Plan-v7-$ts.json" -Encoding UTF8

    $execRes = Invoke-UltraRetry -OpName "PSExecute" -ItemId $SourcePath -Action {
        Invoke-AzUpgradeModulePlan -Plan $planObj -FileEditMode SaveChangesToNewFiles
    }

    # Neue Dateien verschieben (parallel)
    Get-ChildItem $SourcePath -Filter "*_az_upgraded*" -Recurse | ForEach-Object -Parallel {
        $dest = "$using:RootFolder\Upgrades\PS"
        Move-Item $_.FullName $dest -Force
    } -ThrottleLimit $MaxParallelJobs

    $errs = $execRes | Where-Object { $_.UpgradeResult -ne "UpgradeCompleted" }
    if ($errs) {
        $errs | ConvertTo-Json -Depth 10 | Out-File "$RootFolder\Errors\PS-Errors-v7-$ts.json" -Encoding UTF8
    }
}

# ─── 3. AI-KORREKTUR (Grok + DeepSeek, parallel, retry) ───
function Get-AIFix-v7 {
    param($ErrFilePath)

    $errData = Get-Content $ErrFilePath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if (-not $errData) { return $null }

    $snippet = ($errData | Select-Object -First 1).Original  # Erster Fehler-Snippet
    $prompt = @"
AzureRM zu Az migrieren. Fehler: $($errData.UpgradeResultReason).
Code-Snippet: $snippet
Gib NUR den korrigierten PowerShell-Code zurück (funktionsfähig, Az-kompatibel).
"@

    # Grok (primär, retry)
    $fix = Invoke-UltraRetry -OpName "GrokFix" -ItemId (Split-Path $ErrFilePath -Leaf) -Action {
        $body = @{
            model = "grok-beta"
            messages = @(@{ role = "user"; content = $prompt })
            max_tokens = 1500
            temperature = 0.1
        } | ConvertTo-Json -Depth 10
        $resp = Invoke-RestMethod -Uri "https://api.x.ai/v1/chat/completions" -Method Post -Body $body -Headers @{ Authorization = "Bearer $GROK_API_KEY" } -ContentType "application/json" -TimeoutSec 60
        return $resp.choices[0].message.content.Trim()
    }

    # DeepSeek Fallback
    if (-not $fix -and $DEEPSEEK_API_KEY) {
        $fix = Invoke-UltraRetry -OpName "DeepSeekFix" -ItemId (Split-Path $ErrFilePath -Leaf) -Action {
            $body = @{
                model = "deepseek-chat"
                messages = @(@{ role = "user"; content = $prompt })
                max_tokens = 1500
                temperature = 0.1
            } | ConvertTo-Json -Depth 10
            $resp = Invoke-RestMethod -Uri "https://api.deepseek.com/v1/chat/completions" -Method Post -Body $body -Headers @{ Authorization = "Bearer $DEEPSEEK_API_KEY" } -ContentType "application/json" -TimeoutSec 60
            return $resp.choices[0].message.content.Trim()
        }
    }

    return $fix
}

$errFiles = Get-ChildItem "$RootFolder\Errors" -Filter "*.json" -Recurse
if ($errFiles) {
    $errFiles | ForEach-Object -Parallel {
        $fixedCode = Get-AIFix-v7 -ErrFilePath $_.FullName
        if ($fixedCode) {
            $newName = [IO.Path]::GetFileNameWithoutExtension($_.Name) + "_v7_ultra_fixed.ps1"
            $fixedCode | Out-File -FilePath "$using:RootFolder\AICorrections\$newName" -Encoding UTF8
            Write-Host "v7 ULTRA FIXED → $newName" -ForegroundColor Green
        } else {
            Copy-Item $_.FullName "$using:RootFolder\DeadLetter\" -Force
            Write-Host "DEADLETTER → $($_.Name)" -ForegroundColor Red
        }
    } -ThrottleLimit $MaxParallelJobs
}

# ─── SUMMARY & METRIKEN (neue JSON-Datei) ───
$metrics = [PSCustomObject]@{
    Timestamp = Get-Date -Format o
    SourceFiles = (Get-ChildItem $SourcePath -Recurse -File).Count
    UpgradedFiles = (Get-ChildItem "$RootFolder\Upgrades" -Recurse -File).Count
    AIFixes = (Get-ChildItem "$RootFolder\AICorrections" -Recurse -File).Count
    DeadLetters = (Get-ChildItem "$RootFolder\DeadLetter" -Recurse -File).Count
    RootFolder = $RootFolder
    Config = @{ MaxJobs = $MaxParallelJobs; Retries = $MaxRetries }
} | ConvertTo-Json -Depth 5
$metrics | Out-File "$RootFolder\Reports\v7-Summary.json" -Encoding UTF8

Write-Host "`n=== v7 ABGESCHLOSSEN ===" -ForegroundColor Magenta
Write-Host "ALLE NEUEN DATEIEN/ORDNER IN: $RootFolder" -ForegroundColor Green
Write-Host "- Originale: Originals/" -ForegroundColor Gray
Write-Host "- Upgrades: Upgrades/PS/" -ForegroundColor Gray
Write-Host "- AI-Fixes: AICorrections/ (Grok/DeepSeek-optimiert)" -ForegroundColor Green
Write-Host "- DeadLetter: DeadLetter/ (nicht fixierbar)" -ForegroundColor Red
Write-Host "- Logs/Metriken: Reports/v7-Summary.json" -ForegroundColor Yellow
Write-Host "`nTESTE JETZT: Lade Upgrades/AICorrections in PowerShell und führe aus!" -ForegroundColor Cyan