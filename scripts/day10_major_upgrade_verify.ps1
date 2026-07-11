[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 10 major upgrade verification" -ForegroundColor Cyan

$GitStatus = git status --short
if ($GitStatus) {
    Write-Host $GitStatus
}

if ($GitStatus -match "backend[/\\]\.env|frontend[/\\]\.env") {
    throw "Environment file appears in git status. Stop and fix .gitignore before continuing."
}

$RequiredFiles = @(
    "frontend/src/pages/AnalyticsPage.tsx",
    "frontend/src/utils/exportUtils.ts",
    "scripts/day10_major_upgrade_verify.ps1",
    "docs/day-10-major-upgrade-summary.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File)) {
        throw "Required Day 10 file is missing: $File"
    }
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules")) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
}

npm run build

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 10 MAJOR UPGRADE VERIFY PASSED" -ForegroundColor Green
