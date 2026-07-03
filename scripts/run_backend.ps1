[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$VenvPath = Join-Path $ProjectRoot ".venv"
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
$BackendPath = Join-Path $ProjectRoot "backend"

Write-Host "OutcomeIQ backend launcher" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"
Set-Location $ProjectRoot

if (-not (Test-Path -LiteralPath $VenvPath -PathType Container)) {
    Write-Host "Virtual environment not found at $VenvPath" -ForegroundColor Red
    Write-Host "Create it with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
    Write-Host "Activation script not found at $ActivateScript" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath $BackendPath -PathType Container)) {
    Write-Host "Backend folder not found at $BackendPath" -ForegroundColor Red
    exit 1
}

Write-Host "Activating .venv..." -ForegroundColor Green
. $ActivateScript

Set-Location $BackendPath
Write-Host "Starting FastAPI with auto-reload..." -ForegroundColor Green
Write-Host "Swagger UI: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow

uvicorn app.main:app --reload
exit $LASTEXITCODE
