[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 9 frontend polish verification" -ForegroundColor Cyan

$IgnoredPaths = @("backend/.env", "frontend/.env")
foreach ($Path in $IgnoredPaths) {
    git check-ignore --quiet $Path
    if ($LASTEXITCODE -ne 0) {
        throw "$Path is not ignored by Git. Fix .gitignore before continuing."
    }
}

$GitStatus = git status --short
foreach ($Path in $IgnoredPaths) {
    $Pattern = [regex]::Escape($Path)
    if ($GitStatus -match $Pattern) {
        throw "$Path appears in git status. Do not commit environment files."
    }
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules")) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
}

npm run build

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 9 FRONTEND POLISH VERIFY PASSED" -ForegroundColor Green
