[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
Set-Location $ProjectRoot

if ($null -eq (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker was not found. Install and start Docker Desktop." -ForegroundColor Red
    exit 1
}

docker compose exec -T backend python scripts/seed_pricing_rates.py
exit $LASTEXITCODE
