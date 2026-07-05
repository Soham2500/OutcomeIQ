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

Write-Host "OutcomeIQ pre-deployment check" -ForegroundColor Cyan
Write-Host "This script validates readiness; it does not deploy anything." -ForegroundColor DarkCyan

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

    $CurrentStep = "production environment examples"
    $ExamplePaths = @(
        "backend/.env.production.example",
        "frontend/.env.example"
    )
    foreach ($ExamplePath in $ExamplePaths) {
        if (-not (Test-Path -LiteralPath $ExamplePath -PathType Leaf)) {
            throw "Required deployment example is missing: $ExamplePath"
        }
        git check-ignore -q -- $ExamplePath
        if ($LASTEXITCODE -eq 0) {
            throw "$ExamplePath is ignored but must remain trackable."
        }
    }

    $CurrentStep = "backend tests"
    if (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        throw "Virtual environment Python was not found: $VenvPython"
    }
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

    $CurrentStep = "frontend build"
    if ($null -eq (Get-Command npm -ErrorAction SilentlyContinue)) {
        throw "Node/npm is required for the pre-deployment frontend build."
    }
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

    $CurrentStep = "live-quality gate"
    $LiveGatePath = Join-Path $ProjectRoot "scripts\live_quality_gate.ps1"
    if (Test-Path -LiteralPath $LiveGatePath -PathType Leaf) {
        Invoke-RepositoryScript "scripts\live_quality_gate.ps1"
    }
    else {
        throw "The required live-quality gate was not found."
    }

    $Succeeded = $true
}
catch {
    Write-Host "PRE DEPLOY CHECK FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "PRE DEPLOY CHECK PASSED" -ForegroundColor Green
    exit 0
}

exit 1
