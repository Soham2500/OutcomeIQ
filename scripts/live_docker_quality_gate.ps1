[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ConfirmPreference = "None"
$ProgressPreference = "SilentlyContinue"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$PowerShellExecutable = (Get-Process -Id $PID).Path
$CurrentStep = "initialization"
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

function Assert-Endpoint {
    param(
        [string]$Uri,
        [string]$Description
    )

    $Response = Invoke-WebRequest `
        -Uri $Uri `
        -Method Get `
        -TimeoutSec 10 `
        -UseBasicParsing
    if ($Response.StatusCode -lt 200 -or $Response.StatusCode -ge 400) {
        throw "$Description returned HTTP $($Response.StatusCode)."
    }
}

Write-Host "OutcomeIQ live Docker quality gate" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "Docker availability"
    if ($null -eq (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker was not found. Install and start Docker Desktop."
    }
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Desktop is not running."
    }

    $CurrentStep = "base Docker verification"
    Invoke-RepositoryScript "scripts\docker_verify.ps1"

    $CurrentStep = "Docker database migrations"
    Invoke-RepositoryScript "scripts\docker_migrate.ps1"

    $CurrentStep = "Docker pricing seed"
    Invoke-RepositoryScript "scripts\docker_seed_pricing.ps1"

    $CurrentStep = "Docker deterministic demo seed"
    Invoke-RepositoryScript "scripts\docker_seed_demo.ps1"

    $CurrentStep = "Docker backend health"
    Assert-Endpoint `
        "http://127.0.0.1:8000/api/v1/health" `
        "Docker backend health endpoint"

    $CurrentStep = "Docker frontend health"
    Assert-Endpoint `
        "http://127.0.0.1:8080" `
        "Docker frontend"

    $Succeeded = $true
}
catch {
    Write-Host "LIVE DOCKER QUALITY GATE FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "LIVE DOCKER QUALITY GATE PASSED" -ForegroundColor Green
    exit 0
}

exit 1
