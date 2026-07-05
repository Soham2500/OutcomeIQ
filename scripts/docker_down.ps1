[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
Set-Location $ProjectRoot

if ($null -eq (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker was not found. Install and start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Intentionally omits --volumes so local PostgreSQL data is preserved.
docker compose down
exit $LASTEXITCODE
