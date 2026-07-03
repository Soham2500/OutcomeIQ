[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$VenvPath = Join-Path $ProjectRoot ".venv"
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
$BackendPath = Join-Path $ProjectRoot "backend"
$BackendEnv = Join-Path $BackendPath ".env"

Write-Host "OutcomeIQ database readiness check" -ForegroundColor Cyan
Set-Location $ProjectRoot

if (-not (Test-Path -LiteralPath $VenvPath -PathType Container)) {
    Write-Host "DATABASE ERROR" -ForegroundColor Red
    Write-Host "Virtual environment not found at $VenvPath" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
    Write-Host "DATABASE ERROR" -ForegroundColor Red
    Write-Host "Virtual-environment activation script is missing." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path -LiteralPath $BackendEnv -PathType Leaf)) {
    Write-Host "DATABASE NOT CONFIGURED" -ForegroundColor Yellow
    Write-Host "Create backend\.env from backend\.env.example, then set DATABASE_URL." -ForegroundColor Yellow
    exit 0
}

. $ActivateScript
Set-Location $BackendPath

python -m scripts.check_db_connection
exit $LASTEXITCODE
