[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FrontendPath = Join-Path $ProjectRoot "frontend"

if ($null -eq (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "npm was not found. Install Node.js before continuing." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $FrontendPath "package.json") -PathType Leaf)) {
    Write-Host "frontend\package.json was not found." -ForegroundColor Red
    exit 1
}

Push-Location $FrontendPath
try {
    npm install
    if ($LASTEXITCODE -ne 0) {
        throw "npm install failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}

Write-Host "Frontend dependencies installed." -ForegroundColor Green
