[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 13 Razorpay test-mode verification" -ForegroundColor Cyan

$GitStatus = git status --short
if ($GitStatus) {
    Write-Host $GitStatus
}

$TrackedEnvPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env)(\s|$)"
if ($GitStatus -match $TrackedEnvPattern) {
    throw "Environment file appears in git status. Stop and fix .gitignore before continuing."
}

$RequiredFiles = @(
    "backend/app/services/razorpay_service.py",
    "frontend/src/utils/razorpayCheckout.ts",
    "scripts/test_razorpay_webhook.ps1",
    "docs/day-13-razorpay-test-mode.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File)) {
        throw "Required Day 13 file is missing: $File"
    }
}

$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw "Project virtual environment Python not found: $PythonPath"
}

Set-Location -LiteralPath (Join-Path $ProjectRoot "backend")
& $PythonPath -m compileall -q app
& $PythonPath -c "from app.services.razorpay_service import is_configured, verify_webhook_signature; from app.api.v1.router import api_router; print('BACKEND RAZORPAY IMPORT CHECK PASSED')"

Set-Location -LiteralPath (Join-Path $ProjectRoot "frontend")

if (-not (Test-Path -LiteralPath "node_modules")) {
    Write-Host "node_modules missing. Installing declared frontend dependencies..." -ForegroundColor Yellow
    npm install
}

npm run build

Set-Location -LiteralPath $ProjectRoot

Write-Host "DAY 13 RAZORPAY TEST VERIFY PASSED" -ForegroundColor Green
