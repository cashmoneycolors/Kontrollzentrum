#!/usr/bin/env pwsh
<#
.SYNOPSIS
    KONTROLLZENTRUM MONITORING DASHBOARD
    Real-time Überwachung aller Submodules
    
.DESCRIPTION
    - Live-Status aller Submodules
    - Performance-Metriken
    - Fehler-Tracking
    - Automatische Alerts
    - Health-Scores
    
.EXAMPLE
    .\\MONITORING_DASHBOARD.ps1
    .\\MONITORING_DASHBOARD.ps1 -RefreshInterval 10
    .\\MONITORING_DASHBOARD.ps1 -AlertEmail "admin@example.com"

.AUTHOR
    GitHub Copilot | Kontrollzentrum Monitoring
    
.VERSION
    1.0 | 01.12.2025
#>

param(
    [int]$RefreshInterval = 30,
    [string]$AlertEmail = '',
    [bool]$EnableAlerts = $false
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
    MetricsFile = "dashboard_metrics.json"
    AlertLog = "alerts.log"
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

$thresholds = @{
    HealthyScore = 90
    WarningScore = 70
    CriticalScore = 50
    MaxResponseTime = 5000  # ms
    MaxErrorRate = 10       # %
}

# ============================================================================
# MONITORING FUNCTIONS
# ============================================================================

function Get-SubmoduleMetrics {
    param([string]$Submodule)
    
    $name = Split-Path $Submodule -Leaf
    $metrics = @{
        Name = $name
        Path = $Submodule
        Status = 'unknown'
        HealthScore = 0
        Issues = @()
        LastCheck = Get-Date
        ResponseTime = 0
        CommitHash = ''
        Branch = ''
        DirtyFiles = 0
        Conflicts = 0
    }
    
    $startTime = Get-Date
    
    if (-not (Test-Path $Submodule)) {
        $metrics.Status = 'missing'
        $metrics.HealthScore = 0
        $metrics.Issues += "Directory not found"
        $metrics.ResponseTime = (Get-Date) - $startTime
        return $metrics
    }
    
    Push-Location $Submodule
    
    try {
        # Git Status
        $gitStatus = git status --porcelain 2>$null
        $metrics.DirtyFiles = $gitStatus.Count
        
        # Branch
        $metrics.Branch = git rev-parse --abbrev-ref HEAD 2>$null
        
        # Commit
        $metrics.CommitHash = git rev-parse HEAD 2>$null
        
        # Konflikte
        $conflicts = git diff --name-only --diff-filter=U 2>$null
        $metrics.Conflicts = $conflicts.Count
        
        # Remote Status
        $remoteStatus = git status -sb 2>$null
        
        # Health Score Berechnung
        $score = 100
        
        if ($metrics.DirtyFiles -gt 0) {
            $score -= [Math]::Min($metrics.DirtyFiles * 5, 20)
            $metrics.Issues += "Uncommitted changes: $($metrics.DirtyFiles) files"
        }
        
        if ($metrics.Conflicts -gt 0) {
            $score -= $metrics.Conflicts * 10
            $metrics.Issues += "Merge conflicts: $($metrics.Conflicts) files"
        }
        
        if ($remoteStatus -match "behind") {
            $score -= 10
            $metrics.Issues += "Behind remote"
        }
        
        if ($remoteStatus -match "ahead") {
            $score -= 5
            $metrics.Issues += "Ahead of remote"
        }
        
        $metrics.HealthScore = [Math]::Max($score, 0)
        
        # Status bestimmen
        if ($metrics.HealthScore -ge $thresholds.HealthyScore) {
            $metrics.Status = 'healthy'
        } elseif ($metrics.HealthScore -ge $thresholds.WarningScore) {
            $metrics.Status = 'warning'
        } elseif ($metrics.HealthScore -ge $thresholds.CriticalScore) {
            $metrics.Status = 'critical'
        } else {
            $metrics.Status = 'unhealthy'
        }
    }
    catch {
        $metrics.Status = 'error'
        $metrics.HealthScore = 0
        $metrics.Issues += $_.Exception.Message
    }
    
    Pop-Location
    
    $metrics.ResponseTime = (Get-Date) - $startTime
    return $metrics
}

function Get-SystemMetrics {
    $metrics = @{
        Timestamp = Get-Date
        CPU = 0
        Memory = 0
        Disk = 0
        ProcessCount = 0
        Status = 'healthy'
    }
    
    try {
        # CPU
        $cpu = Get-WmiObject win32_processor | Measure-Object -Property LoadPercentage -Average
        $metrics.CPU = $cpu.Average
        
        # Memory
        $os = Get-WmiObject win32_operatingsystem
        $metrics.Memory = [Math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize * 100, 2)
        
        # Disk
        $disk = Get-Volume | Where-Object { $_.DriveLetter -eq 'C' }
        if ($disk) {
            $metrics.Disk = [Math]::Round(($disk.Size - $disk.SizeRemaining) / $disk.Size * 100, 2)
        }
        
        # Process Count
        $metrics.ProcessCount = (Get-Process).Count
        
        # Status
        if ($metrics.CPU -gt 80 -or $metrics.Memory -gt 80 -or $metrics.Disk -gt 90) {
            $metrics.Status = 'warning'
        }
    }
    catch {
        $metrics.Status = 'error'
    }
    
    return $metrics
}

function Show-Dashboard {
    param([array]$SubmoduleMetrics, [hashtable]$SystemMetrics)
    
    Clear-Host
    
    # Header
    Write-Host "╔════════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor $colors.Cyan
    Write-Host "║  🎯 KONTROLLZENTRUM MONITORING DASHBOARD                                      ║" -ForegroundColor $colors.Cyan
    Write-Host "║  Last Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')                                          ║" -ForegroundColor $colors.Cyan
    Write-Host "╚════════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor $colors.Cyan
    
    # System Metrics
    Write-Host "`n📊 SYSTEM METRICS" -ForegroundColor $colors.Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $colors.Gray
    
    $cpuColor = if ($SystemMetrics.CPU -gt 80) { $colors.Red } elseif ($SystemMetrics.CPU -gt 60) { $colors.Yellow } else { $colors.Green }
    $memColor = if ($SystemMetrics.Memory -gt 80) { $colors.Red } elseif ($SystemMetrics.Memory -gt 60) { $colors.Yellow } else { $colors.Green }
    $diskColor = if ($SystemMetrics.Disk -gt 90) { $colors.Red } elseif ($SystemMetrics.Disk -gt 70) { $colors.Yellow } else { $colors.Green }
    
    Write-Host "  CPU:     $($SystemMetrics.CPU.ToString('F1'))% " -NoNewline -ForegroundColor $cpuColor
    Write-Host "[$(Get-ProgressBar $SystemMetrics.CPU 100)]" -ForegroundColor $cpuColor
    
    Write-Host "  Memory:  $($SystemMetrics.Memory.ToString('F1'))% " -NoNewline -ForegroundColor $memColor
    Write-Host "[$(Get-ProgressBar $SystemMetrics.Memory 100)]" -ForegroundColor $memColor
    
    Write-Host "  Disk:    $($SystemMetrics.Disk.ToString('F1'))% " -NoNewline -ForegroundColor $diskColor
    Write-Host "[$(Get-ProgressBar $SystemMetrics.Disk 100)]" -ForegroundColor $diskColor
    
    Write-Host "  Processes: $($SystemMetrics.ProcessCount)" -ForegroundColor $colors.Gray
    
    # Submodule Status
    Write-Host "`n📦 SUBMODULE STATUS" -ForegroundColor $colors.Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $colors.Gray
    
    $healthyCount = 0
    $warningCount = 0
    $criticalCount = 0
    
    foreach ($metric in $SubmoduleMetrics) {
        $icon = switch ($metric.Status) {
            'healthy' { '✅'; $healthyCount++ }
            'warning' { '⚠️'; $warningCount++ }
            'critical' { '❌'; $criticalCount++ }
            'error' { '💀'; $criticalCount++ }
            default { '❓' }
        }
        
        $statusColor = switch ($metric.Status) {
            'healthy' { $colors.Green }
            'warning' { $colors.Yellow }
            'critical' { $colors.Red }
            'error' { $colors.Red }
            default { $colors.Gray }
        }
        
        $scoreBar = Get-ProgressBar $metric.HealthScore 100
        
        Write-Host "  $icon $($metric.Name.PadRight(30)) Score: $($metric.HealthScore.ToString('D3'))/100 [$scoreBar]" -ForegroundColor $statusColor
        
        if ($metric.Issues.Count -gt 0) {
            foreach ($issue in $metric.Issues) {
                Write-Host "     ⚠️  $issue" -ForegroundColor $colors.Yellow
            }
        }
    }
    
    # Summary
    Write-Host "`n📈 SUMMARY" -ForegroundColor $colors.Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $colors.Gray
    
    $total = $SubmoduleMetrics.Count
    $avgScore = ($SubmoduleMetrics | Measure-Object -Property HealthScore -Average).Average
    
    Write-Host "  Total Submodules: $total" -ForegroundColor $colors.Gray
    Write-Host "  Healthy: $healthyCount | Warning: $warningCount | Critical: $criticalCount" -ForegroundColor $colors.Gray
    Write-Host "  Average Health Score: $($avgScore.ToString('F1'))/100" -ForegroundColor $colors.Gray
    
    # Footer
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $colors.Gray
    Write-Host "  Next refresh in $RefreshInterval seconds... (Press Ctrl+C to exit)" -ForegroundColor $colors.Gray
}

function Get-ProgressBar {
    param([int]$Value, [int]$Max, [int]$Width = 20)
    
    $percentage = [Math]::Min([Math]::Max($Value / $Max * 100, 0), 100)
    $filled = [Math]::Round($percentage / 100 * $Width)
    $empty = $Width - $filled
    
    return "█" * $filled + "░" * $empty
}

function Send-Alert {
    param([string]$Subject, [string]$Message, [string]$Severity = 'warning')
    
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $alertEntry = "[$timestamp] [$Severity] $Subject - $Message"
    
    Add-Content -Path $config.AlertLog -Value $alertEntry
    
    if ($EnableAlerts -and $AlertEmail) {
        try {
            Send-MailMessage -To $AlertEmail `
                -From "kontrollzentrum@example.com" `
                -Subject "Kontrollzentrum Alert: $Subject" `
                -Body $Message `
                -SmtpServer "smtp.example.com"
        }
        catch {
            Write-Host "⚠️  Alert email failed: $_" -ForegroundColor $colors.Yellow
        }
    }
}

function Check-Alerts {
    param([array]$SubmoduleMetrics, [hashtable]$SystemMetrics)
    
    # Prüfe Submodule-Alerts
    foreach ($metric in $SubmoduleMetrics) {
        if ($metric.Status -eq 'critical' -or $metric.Status -eq 'error') {
            Send-Alert -Subject "Critical: $($metric.Name)" `
                -Message "Submodule $($metric.Name) is in critical state. Issues: $($metric.Issues -join ', ')" `
                -Severity 'critical'
        }
    }
    
    # Prüfe System-Alerts
    if ($SystemMetrics.CPU -gt 90) {
        Send-Alert -Subject "High CPU Usage" `
            -Message "CPU usage is at $($SystemMetrics.CPU)%" `
            -Severity 'warning'
    }
    
    if ($SystemMetrics.Memory -gt 90) {
        Send-Alert -Subject "High Memory Usage" `
            -Message "Memory usage is at $($SystemMetrics.Memory)%" `
            -Severity 'warning'
    }
    
    if ($SystemMetrics.Disk -gt 95) {
        Send-Alert -Subject "Low Disk Space" `
            -Message "Disk usage is at $($SystemMetrics.Disk)%" `
            -Severity 'critical'
    }
}

function Save-Metrics {
    param([array]$SubmoduleMetrics, [hashtable]$SystemMetrics)
    
    $data = @{
        Timestamp = Get-Date
        System = $SystemMetrics
        Submodules = $SubmoduleMetrics
    }
    
    $data | ConvertTo-Json -Depth 10 | Out-File -Path $config.MetricsFile -Encoding UTF8
}

# ============================================================================
# MAIN LOOP
# ============================================================================

Write-Host "🚀 Starting Kontrollzentrum Monitoring Dashboard..." -ForegroundColor $colors.Green
Write-Host "   Refresh Interval: $RefreshInterval seconds" -ForegroundColor $colors.Gray
Write-Host "   Alerts Enabled: $EnableAlerts" -ForegroundColor $colors.Gray

if (-not $config.RepoRoot) {
    Write-Host "❌ Not in Git repository!" -ForegroundColor $colors.Red
    exit 1
}

$iteration = 0

while ($true) {
    $iteration++
    
    # Sammle Metriken
    $submoduleMetrics = @()
    foreach ($submodule in $config.Submodules) {
        $submoduleMetrics += Get-SubmoduleMetrics $submodule
    }
    
    $systemMetrics = Get-SystemMetrics
    
    # Zeige Dashboard
    Show-Dashboard $submoduleMetrics $systemMetrics
    
    # Prüfe Alerts
    Check-Alerts $submoduleMetrics $systemMetrics
    
    # Speichere Metriken
    Save-Metrics $submoduleMetrics $systemMetrics
    
    # Warte
    Start-Sleep -Seconds $RefreshInterval
}

