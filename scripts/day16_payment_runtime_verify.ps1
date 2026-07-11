[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 16 payment runtime verification" -ForegroundColor Cyan

$GitStatus = git status --short --untracked-files=all
if ($GitStatus) {
    Write-Host $GitStatus
}

$UnsafeStatusPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env|rzp-key\.csv|.*rzp.*\.csv|.*razorpay.*\.csv|.*\.key|.*\.pem|.*\.secret)(\s|$)"
if ($GitStatus -match $UnsafeStatusPattern) {
    throw "Private env, key, pem, secret, or Razorpay CSV appears in git status. Stop before continuing."
}

$RequiredFiles = @(
    "scripts/day16_payment_runtime_smoke.ps1",
    "docs/day-16-payment-runtime-test.md",
    "backend/app/services/razorpay_service.py",
    "backend/app/api/v1/endpoints/billing.py",
    "frontend/src/pages/PricingPage.tsx",
    "frontend/src/pages/BillingPage.tsx"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "Required Day 16 file is missing: $File"
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

Write-Host "DAY 16 PAYMENT RUNTIME VERIFY PASSED" -ForegroundColor Green
