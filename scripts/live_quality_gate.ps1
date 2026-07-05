[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ConfirmPreference = "None"
$ProgressPreference = "SilentlyContinue"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$PowerShellExecutable = (Get-Process -Id $PID).Path
$HealthUrl = "http://127.0.0.1:8000/api/v1/health"
$CurrentStep = "initialization"
$StartedBackend = $false
$BackendProcess = $null
$Succeeded = $false

function Invoke-RepositoryScript {
    param([string]$RelativePath)

    & $PowerShellExecutable `
        -NoProfile `
        -NonInteractive `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot $RelativePath)
    if ($LASTEXITCODE -ne 0) {
        throw "$RelativePath failed with exit code $LASTEXITCODE."
    }
}

function Test-BackendHealth {
    try {
        $Response = Invoke-WebRequest `
            -Uri $HealthUrl `
            -Method Get `
            -TimeoutSec 3 `
            -UseBasicParsing
        return $Response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

Write-Host "OutcomeIQ live-quality MVP gate" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "private environment safety"
    foreach ($EnvironmentPath in @("backend/.env", "frontend/.env")) {
        git check-ignore -q -- $EnvironmentPath
        if ($LASTEXITCODE -ne 0) {
            throw "$EnvironmentPath is not protected by a Git ignore rule."
        }
    }
    $EnvironmentStatus = @(
        git status --short --untracked-files=all |
            Where-Object {
                $_ -match '(^|\s)(backend|frontend)[\\/]\.env$'
            }
    )
    if ($EnvironmentStatus.Count -gt 0) {
        throw "A private environment file appears in Git status."
    }

    $CurrentStep = "virtual environment"
    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        throw "Virtual environment Python was not found: $VenvPython"
    }

    $CurrentStep = "database readiness"
    $DatabaseOutput = & $PowerShellExecutable `
        -NoProfile `
        -NonInteractive `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot "scripts\check_db_ready.ps1") 2>&1
    $DatabaseExitCode = $LASTEXITCODE
    $DatabaseOutput | ForEach-Object { Write-Host $_ }
    $DatabaseLines = @($DatabaseOutput | ForEach-Object { "$($_)".Trim() })
    if ($DatabaseExitCode -ne 0 -or "DATABASE CONNECTED" -notin $DatabaseLines) {
        throw "Database readiness did not report DATABASE CONNECTED."
    }

    $CurrentStep = "static repository verification"
    Invoke-RepositoryScript "scripts\day2_verify.ps1"

    $CurrentStep = "backend tests"
    Push-Location $BackendPath
    try {
        & $VenvPython -m pytest -v
        if ($LASTEXITCODE -ne 0) {
            throw "Backend tests failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }

    $CurrentStep = "frontend verification"
    if (Test-Path -LiteralPath $FrontendPath -PathType Container) {
        if ($null -eq (Get-Command npm -ErrorAction SilentlyContinue)) {
            Write-Host "Node/npm is unavailable; frontend verification was skipped." -ForegroundColor Yellow
            Write-Host "Install Node.js and rerun the gate for complete frontend coverage." -ForegroundColor Yellow
        }
        else {
            Push-Location $FrontendPath
            try {
                if (-not (Test-Path -LiteralPath "node_modules" -PathType Container)) {
                    npm install
                    if ($LASTEXITCODE -ne 0) {
                        throw "Frontend dependency installation failed."
                    }
                }
                npm run build
                if ($LASTEXITCODE -ne 0) {
                    throw "Frontend build failed with exit code $LASTEXITCODE."
                }
            }
            finally {
                Pop-Location
            }
        }
    }
    else {
        Write-Host "Frontend folder is absent; frontend verification was skipped." -ForegroundColor Yellow
    }

    $CurrentStep = "database migrations"
    Invoke-RepositoryScript "scripts\db_migrate.ps1"

    $CurrentStep = "database table verification"
    Invoke-RepositoryScript "scripts\check_db_tables.ps1"

    $CurrentStep = "demo pricing seed"
    Invoke-RepositoryScript "scripts\db_seed_pricing.ps1"

    $CurrentStep = "deterministic demo data seed"
    Invoke-RepositoryScript "scripts\db_seed_demo.ps1"

    $CurrentStep = "backend health detection"
    if (-not (Test-BackendHealth)) {
        $CurrentStep = "background backend startup"
        $BackendProcess = Start-Process `
            -FilePath $VenvPython `
            -ArgumentList @(
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ) `
            -WorkingDirectory $BackendPath `
            -WindowStyle Hidden `
            -PassThru
        $StartedBackend = $true

        $Healthy = $false
        for ($Attempt = 1; $Attempt -le 30; $Attempt++) {
            if ($BackendProcess.HasExited) {
                throw "The backend exited before becoming healthy."
            }
            if (Test-BackendHealth) {
                $Healthy = $true
                break
            }
            Start-Sleep -Seconds 2
        }
        if (-not $Healthy) {
            throw "The backend did not become healthy within 60 seconds."
        }
    }
    else {
        Write-Host "Using the backend already running on port 8000." -ForegroundColor Green
    }

    $SmokeScripts = @(
        "scripts\smoke_auth_project_api.ps1",
        "scripts\smoke_workflow_logging_api.ps1",
        "scripts\smoke_cost_calculation_api.ps1",
        "scripts\smoke_outcome_tracking_api.ps1",
        "scripts\smoke_dashboard_api.ps1",
        "scripts\smoke_recommendation_api.ps1"
    )
    foreach ($SmokeScript in $SmokeScripts) {
        if (Test-Path -LiteralPath (Join-Path $ProjectRoot $SmokeScript) -PathType Leaf) {
            $CurrentStep = "smoke test: $SmokeScript"
            Invoke-RepositoryScript $SmokeScript
        }
        else {
            Write-Host "Skipping missing optional smoke script: $SmokeScript" -ForegroundColor Yellow
        }
    }

    $Succeeded = $true
}
catch {
    Write-Host "LIVE QUALITY GATE FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    if (
        $StartedBackend -and
        $null -ne $BackendProcess -and
        -not $BackendProcess.HasExited
    ) {
        Stop-Process -Id $BackendProcess.Id -ErrorAction SilentlyContinue
        try {
            $BackendProcess.WaitForExit(5000)
        }
        catch {
            # Best-effort cleanup for only the process started by this gate.
        }
        Write-Host "Stopped the backend started by this quality gate." -ForegroundColor Yellow
    }
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "LIVE QUALITY GATE PASSED" -ForegroundColor Green
    exit 0
}

exit 1
