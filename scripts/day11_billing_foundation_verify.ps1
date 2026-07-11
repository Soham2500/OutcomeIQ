[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 11 billing foundation verification" -ForegroundColor Cyan

$GitStatus = git status --short
if ($GitStatus) {
    Write-Host $GitStatus
}

if ($GitStatus -match "backend[/\\]\.env|frontend[/\\]\.env") {
    throw "Environment file appears in git status. Stop and fix .gitignore before continuing."
}

$RequiredFiles = @(
    "backend/app/api/v1/endpoints/billing.py",
    "backend/app/services/billing_service.py",
    "backend/app/services/usage_limit_service.py",
    "frontend/src/api/billingApi.ts",
    "frontend/src/pages/PricingPage.tsx",
    "frontend/src/pages/BillingPage.tsx",
    "docs/subscription-billing-architecture.md",
    "docs/razorpay-test-mode-setup.md",
    "docs/early-live-launch-plan.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File)) {
        throw "Required Day 11 file is missing: $File"
    }
}

$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw "Project virtual environment Python not found: $PythonPath"
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "backend")
& $PythonPath -m compileall -q app
& $PythonPath -c "from app.api.v1.router import api_router; from app.services.billing_service import list_active_plans; from app.services.usage_limit_service import get_usage_summary; print('BACKEND BILLING IMPORT CHECK PASSED')"

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules")) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
}

npm run build

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 11 BILLING FOUNDATION VERIFY PASSED" -ForegroundColor Green
