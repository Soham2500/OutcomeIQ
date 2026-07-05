[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$PowerShellExecutable = (Get-Process -Id $PID).Path
$HealthUrl = "http://127.0.0.1:8000/api/v1/health"
$CurrentStep = "initialization"
$Succeeded = $false

function Invoke-RepositoryScript {
    param([string]$RelativePath)

    & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot $RelativePath)
    if ($LASTEXITCODE -ne 0) {
        throw "$RelativePath failed with exit code $LASTEXITCODE."
    }
}

Write-Host "OutcomeIQ Day 7 dashboard charts verification" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "environment file Git protection"
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

    $CurrentStep = "frontend dependency installation"
    Invoke-RepositoryScript "scripts\install_frontend.ps1"

    $CurrentStep = "frontend typecheck"
    Invoke-RepositoryScript "scripts\frontend_typecheck.ps1"

    $CurrentStep = "database readiness"
    $DatabaseOutput = & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot "scripts\check_db_ready.ps1") 2>&1
    $DatabaseExitCode = $LASTEXITCODE
    $DatabaseOutput | ForEach-Object { Write-Host $_ }
    $DatabaseLines = @($DatabaseOutput | ForEach-Object { "$($_)".Trim() })
    if ($DatabaseExitCode -ne 0 -or "DATABASE CONNECTED" -notin $DatabaseLines) {
        throw "Database readiness did not report DATABASE CONNECTED."
    }

    $CurrentStep = "database migration"
    Invoke-RepositoryScript "scripts\db_migrate.ps1"

    $CurrentStep = "demo pricing seed"
    Invoke-RepositoryScript "scripts\db_seed_pricing.ps1"

    $CurrentStep = "backend health check"
    try {
        $Health = Invoke-RestMethod -Uri $HealthUrl -Method Get -TimeoutSec 5
    }
    catch {
        Write-Host "Start backend first with .\scripts\run_backend.ps1" -ForegroundColor Yellow
        Write-Host "Then rerun this script." -ForegroundColor Yellow
        throw "Backend health endpoint is not reachable."
    }
    if ($Health.status -ne "ok") {
        throw "Backend health endpoint returned an unexpected status."
    }

    $CurrentStep = "API demo data seed"
    Invoke-RepositoryScript "scripts\seed_demo_data_via_api.ps1"
    $Succeeded = $true
}
catch {
    Write-Host "DAY 7 DASHBOARD CHARTS VERIFY FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "DAY 7 DASHBOARD CHARTS VERIFY PASSED" -ForegroundColor Green
    exit 0
}

exit 1
