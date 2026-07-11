[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 15 payment gateway verification" -ForegroundColor Cyan

$GitStatus = git status --short --untracked-files=all
if ($GitStatus) {
    Write-Host $GitStatus
}

$UnsafeStatusPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env|rzp-key\.csv|.*razorpay.*\.csv|.*rzp.*\.csv)(\s|$)"
if ($GitStatus -match $UnsafeStatusPattern) {
    throw "Private env or Razorpay key CSV appears in git status. Stop before continuing."
}

$RequiredFiles = @(
    "backend/app/services/razorpay_service.py",
    "backend/app/api/v1/endpoints/billing.py",
    "frontend/src/utils/razorpayCheckout.ts",
    "frontend/src/api/billingApi.ts",
    "frontend/src/pages/PricingPage.tsx",
    "frontend/src/pages/BillingPage.tsx",
    "docs/day-15-payment-gateway-on.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "Required Day 15 payment gateway file is missing: $File"
    }
}

if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw "Project virtual environment Python not found: $PythonPath"
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "backend")
& $PythonPath -m compileall -q app
if ($LASTEXITCODE -ne 0) {
    throw "Backend compile check failed."
}

& $PythonPath -c "from app.services.razorpay_service import is_configured, is_live_payment_allowed, create_subscription_checkout, verify_webhook_signature, parse_webhook_event; from app.api.v1.router import api_router; print('BACKEND PAYMENT IMPORT CHECK PASSED')"
if ($LASTEXITCODE -ne 0) {
    throw "Backend payment import check failed."
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

Write-Host "DAY 15 PAYMENT GATEWAY VERIFY PASSED" -ForegroundColor Green
