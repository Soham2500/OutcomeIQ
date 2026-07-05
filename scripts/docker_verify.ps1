[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$PowerShellExecutable = (Get-Process -Id $PID).Path
$BackendHealthUrl = "http://127.0.0.1:8000/api/v1/health"
$FrontendUrl = "http://127.0.0.1:8080"
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

function Test-HttpEndpoint {
    param([string]$Uri)

    try {
        $Response = Invoke-WebRequest -Uri $Uri -Method Get -TimeoutSec 5
        return $Response.StatusCode -ge 200 -and $Response.StatusCode -lt 400
    }
    catch {
        return $false
    }
}

function Wait-ForEndpoint {
    param(
        [string]$Uri,
        [string]$Description
    )

    for ($Attempt = 1; $Attempt -le 30; $Attempt++) {
        if (Test-HttpEndpoint $Uri) {
            return
        }
        Start-Sleep -Seconds 2
    }
    throw "$Description did not become reachable within 60 seconds."
}

Write-Host "OutcomeIQ Docker local verification" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "Docker availability"
    if ($null -eq (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker was not found. Install and start Docker Desktop."
    }
    docker compose version *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "The Docker Compose plugin is not available."
    }
    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Desktop is not running."
    }

    $CurrentStep = "Docker image build"
    Invoke-RepositoryScript "scripts\docker_build.ps1"

    $CurrentStep = "Docker service startup"
    Invoke-RepositoryScript "scripts\docker_up.ps1"

    $CurrentStep = "initial backend health"
    Wait-ForEndpoint $BackendHealthUrl "Backend health endpoint"

    $CurrentStep = "database migrations"
    Invoke-RepositoryScript "scripts\docker_migrate.ps1"

    $CurrentStep = "demo pricing seed"
    Invoke-RepositoryScript "scripts\docker_seed_pricing.ps1"

    $CurrentStep = "final backend health"
    Wait-ForEndpoint $BackendHealthUrl "Backend health endpoint"

    $CurrentStep = "frontend availability"
    Wait-ForEndpoint $FrontendUrl "Frontend"

    $Succeeded = $true
}
catch {
    Write-Host "DOCKER LOCAL VERIFY FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
    Write-Host "Inspect containers with: .\scripts\docker_logs.ps1" -ForegroundColor Yellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "DOCKER LOCAL VERIFY PASSED" -ForegroundColor Green
    Write-Host "Backend: $BackendHealthUrl" -ForegroundColor DarkCyan
    Write-Host "Frontend: $FrontendUrl" -ForegroundColor DarkCyan
    exit 0
}

exit 1
