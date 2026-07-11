[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 14 launch-safety verification" -ForegroundColor Cyan

$GitStatus = git status --short --untracked-files=all
if ($GitStatus) {
    Write-Host $GitStatus
}

$TrackedEnvPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env)(\s|$)"
if ($GitStatus -match $TrackedEnvPattern) {
    throw "Private environment file appears in git status. Stop before continuing."
}

$RequiredFiles = @(
    "frontend/src/pages/PrivacyPolicyPage.tsx",
    "frontend/src/pages/TermsPage.tsx",
    "frontend/src/pages/RefundPolicyPage.tsx",
    "frontend/src/pages/ContactPage.tsx",
    "frontend/src/pages/LaunchReadinessPage.tsx",
    "frontend/src/components/LaunchSafetyBanner.tsx",
    "docs/day-14-launch-safety-summary.md",
    "docs/production-payment-go-live-checklist.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "Required Day 14 launch-safety file is missing: $File"
    }
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules" -PathType Container)) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        throw "Frontend dependency installation failed."
    }
}

npm run build
if ($LASTEXITCODE -ne 0) {
    throw "Frontend build failed."
}

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 14 LAUNCH SAFETY VERIFY PASSED" -ForegroundColor Green
