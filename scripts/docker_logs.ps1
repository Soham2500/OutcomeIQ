[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
Set-Location $ProjectRoot

if ($null -eq (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker was not found. Install and start Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host "Following OutcomeIQ container logs. Press Ctrl+C to stop following." -ForegroundColor Cyan
docker compose logs -f
exit $LASTEXITCODE
