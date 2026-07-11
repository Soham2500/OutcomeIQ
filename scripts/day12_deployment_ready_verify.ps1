[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 12 deployment readiness verification" -ForegroundColor Cyan

$GitStatus = git status --short
if ($GitStatus) {
    Write-Host $GitStatus
}

$TrackedEnvPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env)(\s|$)"
if ($GitStatus -match $TrackedEnvPattern) {
    throw "Environment file appears in git status. Stop and fix .gitignore before continuing."
}

$RequiredFiles = @(
    "backend/.env.example",
    "backend/.env.production.example",
    "frontend/.env.example",
    "frontend/vercel.json",
    "scripts/live_smoke_check.ps1",
    "docs/day-12-live-deployment-guide.md",
    "docs/render-vercel-env-vars.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File)) {
        throw "Required Day 12 file is missing: $File"
    }
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules")) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
}

npm run build

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 12 DEPLOYMENT READY VERIFY PASSED" -ForegroundColor Green
