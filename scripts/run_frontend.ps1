[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FrontendPath = Join-Path $ProjectRoot "frontend"

if ($null -eq (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm was not found. Install Node.js before continuing." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $FrontendPath "node_modules") -PathType Container)) {
    Write-Host "Frontend dependencies are missing. Run .\scripts\install_frontend.ps1 first." -ForegroundColor Yellow
    exit 1
}

Set-Location $FrontendPath
npm run dev
exit $LASTEXITCODE
