# Automatisiert Phase 3 des Deployment-Plans: Desktop-Publish, Backend-Bundle und Installer-Staging.
[CmdletBinding()]
param(
    [string]$Configuration = "Release",
    [string]$RuntimeIdentifier = "win-x64",
    [switch]$SkipDesktopPublish,
    [switch]$SkipBackendBuild,
    [switch]$CreateZip,
    [switch]$RegisterService,
    [string]$ReleaseRoot = "release",
    [string]$TaskName = "KontrollzentrumBackend",
    [string]$PwshExecutable = "pwsh.exe"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

function Write-Banner {
    param([string]$Message,[ConsoleColor]$Color = [ConsoleColor]::Green)
    Write-Host "" -ForegroundColor $Color
    Write-Host "╔".PadRight(60,"═") + "╗" -ForegroundColor $Color
    Write-Host "║ $Message".PadRight(59) + "║" -ForegroundColor $Color
    Write-Host "╚".PadRight(60,"═") + "╝" -ForegroundColor $Color
}

function Ensure-Dotnet8 {
    Write-Host "[1/6] Prüfe .NET 8.0 SDK..." -ForegroundColor Cyan
    $dotnetVersion = dotnet --version 2>$null
    if (-not $dotnetVersion -or -not ($dotnetVersion.StartsWith("8."))) {
        throw ".NET 8.* nicht gefunden. Installiere https://dotnet.microsoft.com/download"
    }
    Write-Host "[OK] .NET $dotnetVersion" -ForegroundColor Green
}

function Publish-DesktopApp {
    param([string]$OutputPath)
    Write-Host "[2/6] dotnet publish ($Configuration $RuntimeIdentifier)..." -ForegroundColor Cyan
    if (-not $SkipDesktopPublish) {
        $publishArgs = @(
            "publish",
            "KontrollzentrumDesktop.csproj",
            "-c", $Configuration,
            "-r", $RuntimeIdentifier,
            "/p:PublishSingleFile=true",
            "/p:IncludeNativeLibrariesForSelfExtract=true",
            "/p:PublishTrimmed=false",
            "--self-contained",
            "true",
            "-o", $OutputPath
        )
        dotnet @publishArgs | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "dotnet publish fehlgeschlagen" }
    }
    if (-not (Test-Path $OutputPath)) { throw "Publish-Verzeichnis fehlt: $OutputPath" }
    return $OutputPath
}

function Build-BackendBundle {
    param([string]$BackendExe)
    Write-Host "[3/6] PyInstaller-Bundle prüfen..." -ForegroundColor Cyan
    if (-not $SkipBackendBuild -or -not (Test-Path $BackendExe)) {
        & "$ProjectRoot\build_exe.ps1" | Out-Null
    }
    if (-not (Test-Path $BackendExe)) { throw "Backend-Executable nicht gefunden ($BackendExe). PyInstaller-Run fehlgeschlagen." }
    return $BackendExe
}

function Stage-Release {
    param([string]$DesktopSource,[string]$BackendExePath)
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $releaseFolder = Join-Path $ProjectRoot (Join-Path $ReleaseRoot $stamp)
    $desktopTarget = Join-Path $releaseFolder "DesktopApp"
    $backendTarget = Join-Path $releaseFolder "Backend"
    $configTarget = Join-Path $releaseFolder "Configs"
    $null = New-Item -ItemType Directory -Force -Path $desktopTarget, $backendTarget, $configTarget

    Write-Host "[4/6] Kopiere Desktop-Publish → $desktopTarget" -ForegroundColor Cyan
    Copy-Item -Path (Join-Path $DesktopSource '*') -Destination $desktopTarget -Recurse -Force

    Write-Host "[5/6] Kopiere Backend-Artefakte → $backendTarget" -ForegroundColor Cyan
    Copy-Item -Path $BackendExePath -Destination $backendTarget -Force
    Copy-Item -Path (Join-Path $ProjectRoot "run_services.ps1") -Destination $backendTarget -Force
    Copy-Item -Path (Join-Path $ProjectRoot "requirements.txt") -Destination $backendTarget -Force

    Write-Host "[6/6] Kopiere Konfig-Dateien" -ForegroundColor Cyan
    $envExample = Join-Path $ProjectRoot ".env.example"
    if (Test-Path $envExample) { Copy-Item $envExample $configTarget -Force }
    Copy-Item -Path (Join-Path $ProjectRoot "DEPLOYMENT.md") -Destination $configTarget -Force
    Copy-Item -Path (Join-Path $ProjectRoot "PRODUCTION_CHECKLIST.md") -Destination $configTarget -Force -ErrorAction SilentlyContinue
    Copy-Item -Path (Join-Path $ProjectRoot "README.md") -Destination $configTarget -Force -ErrorAction SilentlyContinue
    $teamLog = Join-Path $ProjectRoot "team_log.txt"
    if (Test-Path $teamLog) {
        Copy-Item $teamLog (Join-Path $configTarget "team_log.txt") -Force
    } else {
        New-Item -ItemType File -Path (Join-Path $configTarget "team_log.txt") | Out-Null
    }
    return $releaseFolder
}

function Write-Checksums {
    param([string]$Target,[string]$ZipArtifact)
    Write-Host "Erzeuge SHA256-Prüfsummen..." -ForegroundColor Cyan
    $checksumFile = Join-Path $Target "checksums.sha256"
    if (Test-Path $checksumFile) { Remove-Item $checksumFile -Force }
    Get-ChildItem -Path $Target -Recurse -File | ForEach-Object {
        $hash = Get-FileHash -Algorithm SHA256 -Path $_.FullName
        $relativePath = $_.FullName.Substring($Target.Length).TrimStart('\')
        "$($hash.Hash) *$relativePath" >> $checksumFile
    }
    if ($ZipArtifact -and (Test-Path $ZipArtifact)) {
        $zipHash = Get-FileHash -Algorithm SHA256 -Path $ZipArtifact
        "$($zipHash.Hash) *$(Split-Path $ZipArtifact -Leaf)" >> $checksumFile
    }
    return $checksumFile
}

function Register-BackendTask {
    param([string]$TaskName,[string]$ScriptPath)
    if (-not (Test-Path $ScriptPath)) { throw "run_services.ps1 nicht gefunden" }
    Write-Host "Registriere Scheduled Task '$TaskName' (At logon)..." -ForegroundColor Cyan
    $action = New-ScheduledTaskAction -Execute $PwshExecutable -Argument "-File `"$ScriptPath`" -Mode prod -RunTeamMode"
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Description "Kontrollzentrum Backend Auto-Start" -Force | Out-Null
}

Write-Banner "🖥️  KONTROLLZENTRUM INSTALLER PIPELINE"
Ensure-Dotnet8

$desktopPublishPath = Join-Path $ProjectRoot "dist\desktop"
$backendExePath = Join-Path $ProjectRoot "dist\🤖ROBOTER_KI_APP.exe"

$desktopSource = Publish-DesktopApp -OutputPath $desktopPublishPath
$backendBinary = Build-BackendBundle -BackendExe $backendExePath
$releaseFolder = Stage-Release -DesktopSource $desktopSource -BackendExePath $backendBinary

if ($RegisterService) {
    Register-BackendTask -TaskName $TaskName -ScriptPath (Join-Path $ProjectRoot "run_services.ps1")
}

$zipPath = $null
if ($CreateZip) {
    $zipName = "Kontrollzentrum_Full_{0}.zip" -f (Split-Path $releaseFolder -Leaf)
    $zipPath = Join-Path (Split-Path $releaseFolder -Parent) $zipName
    Compress-Archive -Path (Join-Path $releaseFolder '*') -DestinationPath $zipPath -Force
}

$checksums = Write-Checksums -Target $releaseFolder -ZipArtifact $zipPath

Write-Banner "✅  PIPELINE ABGESCHLOSSEN"
Write-Host "Release-Ordner:`t$releaseFolder" -ForegroundColor Green
if ($zipPath) { Write-Host "Release-Zip:`t$zipPath" -ForegroundColor Green }
Write-Host "Desktop Publish:`t$desktopSource" -ForegroundColor Green
Write-Host "Backend Binary:`t$backendBinary" -ForegroundColor Green
if ($RegisterService) { Write-Host "Scheduled Task:`t$TaskName" -ForegroundColor Green }
Write-Host "Checksums:`t$checksums" -ForegroundColor Green
Write-Host "Führe Health-Check aus: curl http://localhost:8003/health" -ForegroundColor Cyan
