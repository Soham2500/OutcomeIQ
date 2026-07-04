[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$BackendPath = Join-Path $ProjectRoot "backend"
$ActivateScript = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$PowerShellExecutable = (Get-Process -Id $PID).Path
$HealthUrl = "http://127.0.0.1:8000/api/v1/health"
$CurrentStep = "initialization"
$StartedBackend = $false
$BackendProcess = $null
$Succeeded = $false

function Invoke-RepositoryScript {
    param([string]$RelativePath)

    $ScriptPath = Join-Path $ProjectRoot $RelativePath
    & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File $ScriptPath
    if ($LASTEXITCODE -ne 0) {
        throw "$RelativePath failed with exit code $LASTEXITCODE."
    }
}

function Test-BackendHealth {
    try {
        $Health = Invoke-RestMethod -Uri $HealthUrl -Method Get -TimeoutSec 3
        return $Health.status -eq "ok"
    }
    catch {
        return $false
    }
}

Write-Host "OutcomeIQ Day 5 full verification" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "backend environment Git protection"
    git check-ignore -q -- "backend/.env"
    if ($LASTEXITCODE -ne 0) {
        throw "backend/.env is not protected by a Git ignore rule."
    }
    $GitStatus = @(git status --short --untracked-files=all)
    $EnvironmentStatus = @(
        $GitStatus | Where-Object {
            $_ -match '(^|\s)backend[\\/]\.env$'
        }
    )
    if ($EnvironmentStatus.Count -gt 0) {
        throw "backend/.env appears in Git status. Stop and protect the file."
    }
    Write-Host "backend/.env is ignored by Git." -ForegroundColor Green

    $CurrentStep = "virtual environment activation"
    if (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
        throw "Virtual environment activation script was not found."
    }
    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        throw "Virtual environment Python executable was not found."
    }
    . $ActivateScript

    $CurrentStep = "backend dependency installation"
    & $VenvPython -m pip install -r (Join-Path $BackendPath "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        throw "Dependency installation failed with exit code $LASTEXITCODE."
    }

    $CurrentStep = "database readiness"
    $DatabaseOutput = & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot "scripts\check_db_ready.ps1") 2>&1
    $DatabaseExitCode = $LASTEXITCODE
    $DatabaseOutput | ForEach-Object { Write-Host $_ }
    $DatabaseLines = @($DatabaseOutput | ForEach-Object { "$($_)".Trim() })
    if (
        $DatabaseExitCode -ne 0 -or
        "DATABASE CONNECTED" -notin $DatabaseLines
    ) {
        throw "Database readiness did not report DATABASE CONNECTED."
    }

    $CurrentStep = "project verification"
    Invoke-RepositoryScript "scripts\day2_verify.ps1"

    $CurrentStep = "pytest verification"
    Push-Location $BackendPath
    try {
        & $VenvPython -m pytest -v
        if ($LASTEXITCODE -ne 0) {
            throw "Pytest failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }

    $CurrentStep = "database migration"
    Invoke-RepositoryScript "scripts\db_migrate.ps1"

    $CurrentStep = "required table verification"
    $TableOutput = & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot "scripts\check_db_tables.ps1") 2>&1
    $TableExitCode = $LASTEXITCODE
    $TableOutput | ForEach-Object { Write-Host $_ }
    $TableLines = @($TableOutput | ForEach-Object { "$($_)".Trim() })
    if (
        $TableExitCode -ne 0 -or
        "ALL REQUIRED TABLES EXIST" -notin $TableLines
    ) {
        throw "Required table verification did not pass."
    }

    $CurrentStep = "demo pricing seed"
    Invoke-RepositoryScript "scripts\db_seed_pricing.ps1"

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
                throw "The background backend exited before becoming healthy."
            }
            if (Test-BackendHealth) {
                $Healthy = $true
                break
            }
            Start-Sleep -Seconds 1
        }
        if (-not $Healthy) {
            throw "The background backend did not become healthy within 30 seconds."
        }
    }
    else {
        Write-Host "Using the backend already running on port 8000." -ForegroundColor Green
    }

    $SmokeScripts = @(
        @{ Step = "auth/project API smoke check"; Path = "scripts\smoke_auth_project_api.ps1" },
        @{ Step = "workflow logging API smoke check"; Path = "scripts\smoke_workflow_logging_api.ps1" },
        @{ Step = "cost calculation API smoke check"; Path = "scripts\smoke_cost_calculation_api.ps1" },
        @{ Step = "outcome tracking API smoke check"; Path = "scripts\smoke_outcome_tracking_api.ps1" }
    )
    foreach ($SmokeScript in $SmokeScripts) {
        $CurrentStep = $SmokeScript.Step
        Invoke-RepositoryScript $SmokeScript.Path
    }

    $Succeeded = $true
}
catch {
    Write-Host "DAY 5 FULL VERIFY FAILED" -ForegroundColor Red
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
            # Process cleanup is best-effort after verification.
        }
        Write-Host "Stopped the backend started by this verifier." -ForegroundColor Yellow
    }
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "DAY 5 FULL VERIFY PASSED" -ForegroundColor Green
    exit 0
}

exit 1
