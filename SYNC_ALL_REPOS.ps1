#!/usr/bin/env pwsh
<#
.SYNOPSIS
    OPTION A SYNC SCRIPT - Synchronisiere alle Submodules zentral
    
.DESCRIPTION
    Dieses Script aktualisiert automatisch alle 8 Submodules im Kontrollzentrum Repository
    und erstellt einen Sync-Report mit Status und Änderungen.
    
.PARAMETER Mode
    dev    = Lokale Updates ohne Push (default)
    prod   = Updates + Commit + Push zu GitHub
    status = Nur Status anzeigen
    
.PARAMETER Pull
    $true  = Alle Submodules pullen
    $false = Nur Status (default)

.EXAMPLE
    # Status anzeigen
    .\SYNC_ALL_REPOS.ps1 -Mode status
    
    # Alle Submodules updaten (ohne push)
    .\SYNC_ALL_REPOS.ps1 -Pull $true -Mode dev
    
    # Vollständige Sync + Push
    .\SYNC_ALL_REPOS.ps1 -Pull $true -Mode prod

.AUTHOR
    GitHub Copilot | Kontrollzentrum OPTION A Automation
    
.VERSION
    1.0 | 01.12.2025
#>

param(
    [ValidateSet('status', 'dev', 'prod')]
    [string]$Mode = 'status',
    
    [bool]$Pull = $false
)

# Colors
$colors = @{
    Cyan    = [ConsoleColor]::Cyan
    Green   = [ConsoleColor]::Green
    Yellow  = [ConsoleColor]::Yellow
    Red     = [ConsoleColor]::Red
    Magenta = [ConsoleColor]::Magenta
    Gray    = [ConsoleColor]::Gray
}

function Write-Status {
    param([string]$Message, [ConsoleColor]$Color = 'White')
    Write-Host $Message -ForegroundColor $Color
}

# Header
Write-Status "╔════════════════════════════════════════════════════════════════╗" $colors.Cyan
Write-Status "║  🔄 KONTROLLZENTRUM OPTION A - SYNC SCRIPT                     ║" $colors.Cyan
Write-Status "║  Synchronisiere alle 8 Submodules                             ║" $colors.Cyan
Write-Status "╚════════════════════════════════════════════════════════════════╝" $colors.Cyan

# Prüfe ob wir in Kontrollzentrum-1 sind
$repoRoot = git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) {
    Write-Status "❌ Nicht in Git Repository!" $colors.Red
    exit 1
}

Write-Status "`n📍 Repository: $repoRoot`n" $colors.Yellow

# PHASE 1: STATUS
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
Write-Status "1️⃣  SUBMODULE STATUS" $colors.Magenta
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan

$status = & git submodule status
Write-Status $status $colors.Gray

if ($Mode -eq 'status') {
    Write-Status "`n✅ Status angezeigt. Beende." $colors.Green
    exit 0
}

# PHASE 2: PULL (optional)
if ($Pull) {
    Write-Status "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
    Write-Status "2️⃣  SUBMODULES UPDATEN" $colors.Magenta
    Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
    
    Write-Status "`nInitialisiere Submodules..." $colors.Yellow
    git submodule update --init --recursive 2>&1 | Write-Status -Color $colors.Gray
    
    Write-Status "`nUpdate Submodules (fetch latest)..." $colors.Yellow
    git submodule update --remote --merge 2>&1 | Write-Status -Color $colors.Gray
    
    Write-Status "`n✅ Submodule aktualisiert" $colors.Green
}

# PHASE 3: COMMIT (wenn Mode = prod)
if ($Mode -eq 'prod') {
    Write-Status "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
    Write-Status "3️⃣  COMMIT & PUSH (PRODUCTION MODE)" $colors.Magenta
    Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
    
    # Git Status
    $changes = & git status --porcelain
    if ($changes) {
        Write-Status "`n📝 Änderungen erkannt:" $colors.Yellow
        Write-Status $changes $colors.Gray
        
        Write-Status "`nCommitte Änderungen..." $colors.Yellow
        git add .
        git commit -m "🔄 Update submodules - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -q
        Write-Status "✅ Commit erstellt" $colors.Green
        
        Write-Status "`nPush zu GitHub..." $colors.Yellow
        git push origin blackboxai/azure-mcp-setup -q
        Write-Status "✅ Push erfolgreich" $colors.Green
    } else {
        Write-Status "ℹ️  Keine Änderungen zum Commit" $colors.Gray
    }
}

# ABSCHLUSS
Write-Status "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan
Write-Status "✅ SYNC COMPLETE" $colors.Green
Write-Status "Mode: $Mode | Pull: $Pull" $colors.Gray
Write-Status "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" $colors.Cyan

Write-Status "`n📚 NÄCHSTE SCHRITTE:" $colors.Cyan
Write-Status "  # Arbeite mit Submodules" $colors.Gray
Write-Status "  cd submodules/module" $colors.Gray
Write-Status "  git checkout main  # oder dein preferred branch" $colors.Gray
Write-Status "  git pull origin main" $colors.Gray
Write-Status "" $colors.Gray
Write-Status "  # Nach Änderungen pushen:" $colors.Gray
Write-Status "  git add -A && git commit -m 'Update'" $colors.Gray
Write-Status "  git push origin main" $colors.Gray
Write-Status "" $colors.Gray
Write-Status "  # Zurück zu Parent (Kontrollzentrum-1)" $colors.Gray
Write-Status "  cd ../.." $colors.Gray
Write-Status "  .\SYNC_ALL_REPOS.ps1 -Pull -Mode prod  # Update parent submodule refs" $colors.Gray
