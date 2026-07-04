[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FrontendPath = Join-Path $ProjectRoot "frontend"

if ($null -eq (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm was not found. Install Node.js before continuing." -ForegroundColor Red
    exit 1
}

Push-Location $FrontendPath
try {
    npm run typecheck
    if ($LASTEXITCODE -ne 0) {
        throw "Frontend typecheck failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

Write-Host "Frontend typecheck passed." -ForegroundColor Green
