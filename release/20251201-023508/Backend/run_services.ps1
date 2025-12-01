# Automatisiert den Start der FastAPI-Services inkl. Key-Check und Health-Monitoring.
# Beispiel: .\run_services.ps1 -Mode prod -RunTeamMode
[CmdletBinding()]
param(
	[ValidateSet("dev", "prod")]
	[string]$Mode = "dev",
	[int]$Port = 8003,
	[switch]$RunTeamMode,
	[int]$HealthTimeoutSec = 90,
	[int]$HealthIntervalSec = 3,
	[string]$LogDirectory = "logs"
)

$ErrorActionPreference = "Stop"

function Write-Section {
	param([string]$Message)
	Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot
Write-Section "Kontrollzentrum Backend Automation"
Write-Host "Projektpfad:`t$ProjectRoot"

$envPath = Join-Path $ProjectRoot ".env"
if (-not (Test-Path $envPath)) {
	throw ".env nicht gefunden. Bitte alle REQUIRED_KEYS setzen."
}

function Resolve-PythonLauncher {
	$py = Get-Command py -ErrorAction SilentlyContinue
	if ($py) {
		return @{ Executable = $py.Source; Args = @("-3.13") }
	}
	$python = Get-Command python -ErrorAction SilentlyContinue
	if ($python) {
		return @{ Executable = $python.Source; Args = @() }
	}
	throw "Python Launcher 'py' oder 'python' wurde nicht gefunden."
}

$pythonLauncher = Resolve-PythonLauncher
$PythonExecutable = $pythonLauncher.Executable
$PythonArgs = $pythonLauncher.Args
Write-Host "Python:`t$PythonExecutable $($PythonArgs -join ' ')"

function Invoke-PythonCommand {
	param(
		[string[]]$Arguments,
		[switch]$ThrowOnError
	)

	$fullArgs = @()
	if ($PythonArgs) { $fullArgs += $PythonArgs }
	$fullArgs += $Arguments
	& $PythonExecutable @fullArgs
	if ($LASTEXITCODE -ne 0 -and $ThrowOnError) {
		throw "Python-Befehl fehlgeschlagen: $($Arguments -join ' ')"
	}
}

Write-Section "Prüfe REQUIRED_KEYS"
Invoke-PythonCommand -Arguments @("-c", "from core.key_check import check_all_keys; check_all_keys()") -ThrowOnError
Write-Host "Alle Keys vorhanden."

$logRoot = if ([System.IO.Path]::IsPathRooted($LogDirectory)) { $LogDirectory } else { Join-Path $ProjectRoot $LogDirectory }
if (-not (Test-Path $logRoot)) {
	New-Item -ItemType Directory -Path $logRoot | Out-Null
}
$fastApiStdOut = Join-Path $logRoot "fastapi-out.log"
$fastApiStdErr = Join-Path $logRoot "fastapi-err.log"
New-Item -ItemType File -Force -Path $fastApiStdOut | Out-Null
New-Item -ItemType File -Force -Path $fastApiStdErr | Out-Null

function Start-BackendService {
	param([int]$ServicePort)

	$args = @()
	if ($PythonArgs) { $args += $PythonArgs }
	$args += @("-m", "uvicorn", "modules.ki_sideboard:app", "--host", "0.0.0.0", "--port", $ServicePort.ToString(), "--log-level", "info")
	if ($Mode -eq "dev") {
		$args += "--reload"
	}

	Write-Section "Starte ki_sideboard (Port $ServicePort)"
	$process = Start-Process -FilePath $PythonExecutable -ArgumentList $args -WorkingDirectory $ProjectRoot -NoNewWindow -PassThru -RedirectStandardOutput $fastApiStdOut -RedirectStandardError $fastApiStdErr
	Write-Host "PID:`t$($process.Id)"
	return $process
}

function Test-ServiceHealth {
	param(
		[string]$Url,
		[int]$TimeoutSec = 60,
		[int]$IntervalSec = 2
	)

	$deadline = (Get-Date).AddSeconds($TimeoutSec)
	while ((Get-Date) -lt $deadline) {
		try {
			$response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
			if ($response.StatusCode -eq 200) {
				return $true
			}
		}
		catch {
			Start-Sleep -Seconds $IntervalSec
		}
	}
	throw "Service unter $Url ist nicht erreichbar."
}

function Show-TeamLogTail {
	param([int]$Lines = 30)
	$teamLog = Join-Path $ProjectRoot "team_log.txt"
	if (Test-Path $teamLog) {
		Write-Section "team_log (letzte $Lines Zeilen)"
		Get-Content -Path $teamLog -Tail $Lines
	}
	else {
		Write-Host "team_log.txt nicht gefunden." -ForegroundColor Yellow
	}
}

$backendProcess = $null
try {
	$backendProcess = Start-BackendService -ServicePort $Port
	$healthUrl = "http://127.0.0.1:$Port/health"
	Write-Section "Health-Check"
	Test-ServiceHealth -Url $healthUrl -TimeoutSec $HealthTimeoutSec -IntervalSec $HealthIntervalSec | Out-Null
	Write-Host "Health-Check erfolgreich: $healthUrl"

	if ($RunTeamMode) {
		Write-Section "Starte Team-Modus"
		Invoke-PythonCommand -Arguments @("main.py", "team") -ThrowOnError
		Show-TeamLogTail -Lines 40
	}

	Write-Section "Laufzeit"
	Write-Host "Logs:`t$fastApiStdOut"
	Write-Host "Beenden mit Ctrl+C."
	Wait-Process -Id $backendProcess.Id
}
finally {
	if ($backendProcess -and -not $backendProcess.HasExited) {
		Write-Host "Stoppe Backend (PID $($backendProcess.Id))" -ForegroundColor Yellow
		Stop-Process -Id $backendProcess.Id -Force
	}
}