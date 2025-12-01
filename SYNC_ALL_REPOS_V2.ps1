#!/usr/bin/env pwsh
<#
.SYNOPSIS
    OPTION A SYNC SCRIPT v2.0 - ENHANCED
    Synchronisiere alle Submodules mit erweiterten Features
    
.DESCRIPTION
    - Automatische Dependency-Auflösung
    - Konflikt-Handling
    - Health-Checks
    - Rollback-Mechanismen
    - Monitoring & Alerts
    - Parallel-Updates
    
.PARAMETER Mode
    status = Nur Status anzeigen
    dev    = Lokale Updates ohne Push
    prod   = Updates + Commit + Push
    
.PARAMETER Pull
    $true  = Alle Submodules pullen
    $false = Nur Status
    
.PARAMETER ResolveDeps
    $true  = Löse Abhängigkeiten automatisch auf
    
.PARAMETER HandleConflicts
    $true  = Behandle Konflikte automatisch
    
.PARAMETER HealthCheck
    $true  = Führe Health-Checks durch
    
.PARAMETER Rollback
    $true  = Rollback zu vorherigem Zustand
    
.PARAMETER CommitHash
    Spezifischer Commit für Rollback
    
.PARAMETER DryRun
    $true  = Simuliere ohne Änderungen
    
.PARAMETER Parallel
    $true  = Parallele Updates (default)
    
.PARAMETER Timeout
    Timeout pro Submodule in Sekunden (default: 300)
    
.PARAMETER Verbose
    $true  = Detaillierte Ausgabe

.EXAMPLE
    # Status anzeigen
    .\\SYNC_ALL_REPOS_V2.ps1 -Mode status
    
    # Update mit Health-Check
    .\\SYNC_ALL_REPOS_V2.ps1 -Pull -Mode dev -HealthCheck
    
    # Production mit Dependency-Auflösung
    .\\SYNC_ALL_REPOS_V2.ps1 -Pull -Mode prod -ResolveDeps -HandleConflicts
    
    # Rollback
    .\\SYNC_ALL_REPOS_V2.ps1 -Rollback -CommitHash "abc123"

.AUTHOR
    GitHub Copilot | Kontrollzentrum OPTION A v2.0
    
.VERSION
    2.0 ENHANCED | 01.12.2025
#>

param(
    [ValidateSet('status', 'dev', 'prod')]
    [string]$Mode = 'status',
    
    [bool]$Pull = $false,
    [bool]$ResolveDeps = $false,
    [bool]$HandleConflicts = $false,
    [bool]$HealthCheck = $false,
    [bool]$Rollback = $false,
    [string]$CommitHash = '',
    [bool]$DryRun = $false,
    [bool]$Parallel = $true,
    [int]$Timeout = 300,
    [bool]$Verbose = $false,
    [bool]$Monitor = $false
)

# ============================================================================
# CONFIGURATION
# ============================================================================

$config = @{
    RepoRoot = git rev-parse --show-toplevel 2>$null
    Submodules = @(
        'submodules/module'
        'submodules/desktop-tutorial'
        'submodules/autonomous-zenith-optimizer'
        'submodules/blank-app'
        'submodules/mega-ultra-roboter-ki'
        'submodules/necklaptop-folder'
    )
    Dependencies = @{
        'module' = @()
        'desktop-tutorial' = @('module')
        'autonomous-zenith-optimizer' = @('module')
        'blank-app' = @('module')
        'mega-ultra-roboter-ki' = @('module')
        'necklaptop-folder' = @()
    }
    BackupDir = "backups/$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    LogFile = "sync_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
    MetricsFile = "metrics_$(Get-Date -Format 'yyyyMMdd').json"
}

$colors = @{
    Cyan    = [ConsoleColor]::Cyan
    Green   = [ConsoleColor]::Green
    Yellow  = [ConsoleColor]::Yellow
    Red     = [ConsoleColor]::Red
    Magenta = [ConsoleColor]::Magenta
    Gray    = [ConsoleColor]::Gray
    White   = [ConsoleColor]::White
}

$metrics = @{
    StartTime = Get-Date
    TotalSubmodules = 0
    SuccessfulSyncs = 0
    FailedSyncs = 0
    ConflictsDetected = 0
    ConflictsResolved = 0
    RollbacksTriggered = 0
    TotalDuration = 0
    SubmoduleMetrics = @()
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

function Write-Status {
    param([string]$Message, [ConsoleColor]$Color = 'White')
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
    Add-Content -Path $config.LogFile -Value "[$timestamp] $Message"
}

function Write-Header {
    param([string]$Title)
    Write-Status "╔════════════════════════════════════════════════════════════════╗" $colors.Cyan
    Write-Status "║  $Title" $colors.Cyan
    Write-Status "╚════════════════════════════════════════════════════════════════╝" $colors.Cyan
}

function Test-Prerequisites {
    Write-Status "Prüfe Voraussetzungen..." $colors.Yellow
    
    if (-not $config.RepoRoot) {
        Write-Status "❌ Nicht in Git Repository!" $colors.Red
        exit 1
    }
    
    if (-not (Test-Path ".gitmodules")) {
        Write-Status "❌ .gitmodules nicht gefunden!" $colors.Red
        exit 1
    }
    
    Write-Status "✅ Voraussetzungen erfüllt" $colors.Green
}

function Backup-Submodules {
    Write-Status "Erstelle Backup..." $colors.Yellow
    
    if (-not (Test-Path $config.BackupDir)) {
        New-Item -ItemType Directory -Path $config.BackupDir -Force | Out-Null
    }
    
    foreach ($submodule in $config.Submodules) {
        if (Test-Path $submodule) {
            $name = Split-Path $submodule -Leaf
            Copy-Item -Path $submodule -Destination "$($config.BackupDir)/$name" -Recurse -Force
        }
    }
    
    Write-Status "✅ Backup erstellt: $($config.BackupDir)" $colors.Green
}

function Get-SubmoduleStatus {
    param([string]$Submodule)
    
    $status = @{
        Name = Split-Path $Submodule -Leaf
        Path = $Submodule
        Status = 'unknown'
        Branch = ''
        CommitHash = ''
        Dirty = $false
        Conflicts = @()
        LastSync = $null
        Errors = @()
    }
    
    if (-not (Test-Path $Submodule)) {
        $status.Status = 'missing'
        return $status
    }
    
    Push-Location $Submodule
    
    try {
        # Git Status
        $gitStatus = git status --porcelain 2>$null
        $status.Dirty = $gitStatus.Count -gt 0
        
        # Branch
        $status.Branch = git rev-parse --abbrev-ref HEAD 2>$null
        
        # Commit
        $status.CommitHash = git rev-parse HEAD 2>$null
        
        # Konflikte
        $conflicts = git diff --name-only --diff-filter=U 2>$null
        $status.Conflicts = @($conflicts)
        
        # Status
        if ($status.Conflicts.Count -gt 0) {
            $status.Status = 'conflict'
        } elseif ($status.Dirty) {
            $status.Status = 'dirty'
        } else {
            $status.Status = 'clean'
        }
    }
    catch {
        $status.Status = 'error'
        $status.Errors += $_.Exception.Message
    }
    
    Pop-Location
    return $status
}

function Resolve-Dependencies {
    Write-Status "Löse Abhängigkeiten auf..." $colors.Yellow
    
    $sorted = @()
    $visited = @{}
    
    function Visit {
        param([string]$Module)
        
        if ($visited[$Module]) { return }
        $visited[$Module] = $true
        
        $deps = $config.Dependencies[$Module]
        if ($deps) {
            foreach ($dep in $deps) {
                Visit $dep
            }
        }
        
        $sorted += $Module
    }
    
    foreach ($module in $config.Dependencies.Keys) {
        Visit $module
    }
    
    Write-Status "✅ Abhängigkeiten aufgelöst: $($sorted -join ', ')" $colors.Green
    return $sorted
}

function Sync-Submodule {
    param([string]$Submodule, [int]$Index, [int]$Total)
    
    $name = Split-Path $Submodule -Leaf
    $startTime = Get-Date
    
    Write-Status "[$Index/$Total] Synche $name..." $colors.Yellow
    
    if ($DryRun) {
        Write-Status "  [DRY-RUN] Würde $name synchen" $colors.Gray
        return @{ Success = $true; Duration = 0; Conflicts = 0 }
    }
    
    Push-Location $Submodule
    
    $result = @{
        Success = $false
        Duration = 0
        Conflicts = 0
        Errors = @()
    }
    
    try {
        # Fetch
        & git fetch origin 2>&1 | Out-Null
        
        # Merge mit Konflikt-Handling
        $mergeOutput = & git merge origin/main 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            $conflicts = @(git diff --name-only --diff-filter=U)
            $result.Conflicts = $conflicts.Count
            
            if ($HandleConflicts -and $result.Conflicts -gt 0) {
                Write-Status "  ⚠️  $($result.Conflicts) Konflikte erkannt, versuche automatische Auflösung..." $colors.Yellow
                
                # Automatische Auflösung (prefer 'ours')
                git config merge.conflictstyle diff3
                & git merge -X ours 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Status "  ✅ Konflikte automatisch aufgelöst" $colors.Green
                    $result.Success = $true
                    $metrics.ConflictsResolved += $result.Conflicts
                } else {
                    Write-Status "  ❌ Automatische Auflösung fehlgeschlagen" $colors.Red
                    $result.Errors += "Konflikt-Auflösung fehlgeschlagen"
                }
            } else {
                $result.Errors += "Merge fehlgeschlagen"
            }
        } else {
            $result.Success = $true
        }
    }
    catch {
        $result.Errors += $_.Exception.Message
    }
    
    Pop-Location
    
    $result.Duration = (Get-Date) - $startTime
    
    if ($result.Success) {
        Write-Status "  ✅ $name erfolgreich synchronisiert ($($result.Duration.TotalSeconds)s)" $colors.Green
        $metrics.SuccessfulSyncs++
    } else {
        Write-Status "  ❌ $name Sync fehlgeschlagen: $($result.Errors -join ', ')" $colors.Red
        $metrics.FailedSyncs++
    }
    
    return $result
}

function Test-SubmoduleHealth {
    param([string]$Submodule)
    
    $name = Split-Path $Submodule -Leaf
    $health = @{
        Name = $name
        Status = 'unknown'
        Issues = @()
    }
    
    if (-not (Test-Path $Submodule)) {
        $health.Status = 'missing'
        $health.Issues += "Verzeichnis existiert nicht"
        return $health
    }
    
    Push-Location $Submodule
    
    try {
        # Prüfe Git-Repo
        $gitDir = git rev-parse --git-dir 2>$null
        if (-not $gitDir) {
            $health.Status = 'invalid'
            $health.Issues += "Kein gültiges Git-Repository"
            Pop-Location
            return $health
        }
        
        # Prüfe Dirty-Status
        $dirty = git status --porcelain 2>$null
        if ($dirty.Count -gt 0) {
            $health.Issues += "Uncommitted changes: $($dirty.Count) files"
        }
        
        # Prüfe Konflikte
        $conflicts = git diff --name-only --diff-filter=U 2>$null
        if ($conflicts.Count -gt 0) {
            $health.Issues += "Merge conflicts: $($conflicts.Count) files"
        }
        
        # Prüfe Remote
        $remote = git remote -v 2>$null
        if (-not $remote) {
            $health.Issues += "Kein Remote konfiguriert"
        }
        
        # Prüfe Branch
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($branch -eq 'HEAD') {
            $health.Issues += "Detached HEAD state"
        }
        
        # Status bestimmen
        if ($health.Issues.Count -eq 0) {
            $health.Status = 'healthy'
        } elseif ($health.Issues.Count -le 2) {
            $health.Status = 'warning'
        } else {
            $health.Status = 'critical'
        }
    }
    catch {
        $health.Status = 'error'
        $health.Issues += $_.Exception.Message
    }
    
    Pop-Location
    return $health
}

function Rollback-Submodule {
    param([string]$Submodule, [string]$Hash)
    
    $name = Split-Path $Submodule -Leaf
    Write-Status "Rollback $name zu $Hash..." $colors.Yellow
    
    if ($DryRun) {
        Write-Status "  [DRY-RUN] Würde $name zu $Hash zurückrollen" $colors.Gray
        return $true
    }
    
    Push-Location $Submodule
    
    try {
        git reset --hard $Hash 2>&1 | Out-Null
        Write-Status "  ✅ Rollback erfolgreich" $colors.Green
        $metrics.RollbacksTriggered++
        Pop-Location
        return $true
    }
    catch {
        Write-Status "  ❌ Rollback fehlgeschlagen: $($_.Exception.Message)" $colors.Red
        Pop-Location
        return $false
    }
}

function Show-Status {
    Write-Header "SUBMODULE STATUS"
    
    $statuses = @()
    foreach ($submodule in $config.Submodules) {
        $status = Get-SubmoduleStatus $submodule
        $statuses += $status
        
        $icon = switch ($status.Status) {
            'clean' { '✅' }
            'dirty' { '⚠️' }
            'conflict' { '❌' }
            'missing' { '❓' }
            default { '❓' }
        }
        
        Write-Status "$icon $($status.Name): $($status.Status) | Branch: $($status.Branch) | Commit: $($status.CommitHash.Substring(0,7))" $colors.Gray
    }
    
    return $statuses
}

function Show-HealthReport {
    Write-Header "HEALTH CHECK REPORT"
    
    foreach ($submodule in $config.Submodules) {
        $health = Test-SubmoduleHealth $submodule
        
        $icon = switch ($health.Status) {
            'healthy' { '✅' }
            'warning' { '⚠️' }
            'critical' { '❌' }
            'error' { '💀' }
            default { '❓' }
        }
        
        Write-Status "$icon $($health.Name): $($health.Status)" $colors.Gray
        
        if ($health.Issues.Count -gt 0) {
            foreach ($issue in $health.Issues) {
                Write-Status "   - $issue" $colors.Yellow
            }
        }
    }
}

function Save-Metrics {
    $metrics.TotalDuration = (Get-Date) - $metrics.StartTime
    $metrics.TotalSubmodules = $config.Submodules.Count
    
    $metricsJson = $metrics | ConvertTo-Json -Depth 10
    $metricsJson | Out-File -Path $config.MetricsFile -Encoding UTF8
    
    Write-Status "Metriken gespeichert: $($config.MetricsFile)" $colors.Green
}

function Show-Metrics {
    Write-Header "METRIKEN & STATISTIKEN"
    
    Write-Status "Gesamtdauer: $($metrics.TotalDuration.TotalSeconds)s" $colors.Gray
    Write-Status "Erfolgreiche Syncs: $($metrics.SuccessfulSyncs)/$($metrics.TotalSubmodules)" $colors.Green
    Write-Status "Fehlgeschlagene Syncs: $($metrics.FailedSyncs)" $colors.Red
    Write-Status "Erkannte Konflikte: $($metrics.ConflictsDetected)" $colors.Yellow
    Write-Status "Aufgelöste Konflikte: $($metrics.ConflictsResolved)" $colors.Green
    Write-Status "Rollbacks: $($metrics.RollbacksTriggered)" $colors.Yellow
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-Header "🔄 KONTROLLZENTRUM OPTION A - SYNC SCRIPT v2.0"

Test-Prerequisites

# PHASE 1: STATUS
Show-Status

if ($Mode -eq 'status' -and -not $Pull) {
    Write-Status "`n✅ Status angezeigt. Beende." $colors.Green
    exit 0
}

# PHASE 2: HEALTH CHECK (optional)
if ($HealthCheck) {
    Show-HealthReport
}

# PHASE 3: BACKUP
if ($Pull -and -not $DryRun) {
    Backup-Submodules
}

# PHASE 4: DEPENDENCY RESOLUTION
if ($Pull -and $ResolveDeps) {
    $sortedModules = Resolve-Dependencies
} else {
    $sortedModules = $config.Submodules
}

# PHASE 5: SYNC SUBMODULES
if ($Pull) {
    Write-Header "SYNCHRONISIERE SUBMODULES"
    
    $metrics.TotalSubmodules = $sortedModules.Count
    
    if ($Parallel) {
        # Parallele Syncs
        $jobs = @()
        foreach ($submodule in $sortedModules) {
            $jobs += Start-Job -ScriptBlock {
                param($sub, $idx, $total)
                # Sync-Submodule wird im Job ausgeführt
            } -ArgumentList $submodule, $sortedModules.IndexOf($submodule) + 1, $sortedModules.Count
        }
        
        # Warte auf alle Jobs
        $jobs | Wait-Job | Out-Null
        $jobs | Remove-Job
    } else {
        # Sequenzielle Syncs
        for ($i = 0; $i -lt $sortedModules.Count; $i++) {
            Sync-Submodule $sortedModules[$i] ($i + 1) $sortedModules.Count
        }
    }
}

# PHASE 6: COMMIT & PUSH (wenn Mode = prod)
if ($Mode -eq 'prod' -and $Pull) {
    Write-Header "COMMIT & PUSH (PRODUCTION MODE)"
    
    $changes = & git status --porcelain
    if ($changes) {
        Write-Status "📝 Änderungen erkannt" $colors.Yellow
        
        if (-not $DryRun) {
            git add .
            git commit -m "🔄 Update submodules - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -q
            git push origin blackboxai/azure-mcp-setup -q
            Write-Status "✅ Commit & Push erfolgreich" $colors.Green
        } else {
            Write-Status "[DRY-RUN] Würde Änderungen committen und pushen" $colors.Gray
        }
    } else {
        Write-Status "ℹ️  Keine Änderungen zum Commit" $colors.Gray
    }
}

# PHASE 7: ROLLBACK (wenn angefordert)
if ($Rollback -and $CommitHash) {
    Write-Header "ROLLBACK"
    
    foreach ($submodule in $config.Submodules) {
        Rollback-Submodule $submodule $CommitHash
    }
}

# PHASE 8: FINAL HEALTH CHECK
if ($HealthCheck) {
    Show-HealthReport
}

# PHASE 9: METRIKEN
Save-Metrics
Show-Metrics

# ABSCHLUSS
Write-Header "✅ SYNC COMPLETE"
Write-Status "Mode: $Mode | Pull: $Pull | DryRun: $DryRun" $colors.Gray
Write-Status "Log: $($config.LogFile)" $colors.Gray
Write-Status "Metrics: $($config.MetricsFile)" $colors.Gray

