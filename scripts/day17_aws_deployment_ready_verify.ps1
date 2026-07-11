[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))

Set-Location -LiteralPath $ProjectRoot

Write-Host "OutcomeIQ Day 17 AWS deployment readiness verification" -ForegroundColor Cyan

$GitStatus = git status --short --untracked-files=all
if ($GitStatus) {
    Write-Host $GitStatus
}

$UnsafeStatusPattern = "(^|\n)\s*(\S+\s+)?(backend[/\\]\.env|frontend[/\\]\.env|rzp-key\.csv|.*rzp.*\.csv|.*razorpay.*\.csv|.*\.key|.*\.pem|.*\.secret|.*[/\\]\.aws[/\\].*|.*[/\\]credentials|.*[/\\]config)(\s|$)"
if ($GitStatus -match $UnsafeStatusPattern) {
    throw "Private env, payment key, or AWS credential file appears in git status. Stop before continuing."
}

$RequiredFiles = @(
    "docker-compose.aws.yml",
    "backend/.env.aws.example",
    "frontend/amplify.yml",
    "scripts/aws_lightsail_server_setup.sh",
    "scripts/aws_lightsail_deploy_commands.md",
    "scripts/aws_live_smoke_check.ps1",
    "docs/day-17-aws-deployment-guide.md",
    "docs/aws-lightsail-env-vars.md",
    "docs/aws-cost-safety-checklist.md"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "Required Day 17 AWS deployment file is missing: $File"
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

Write-Host "DAY 17 AWS DEPLOYMENT READY VERIFY PASSED" -ForegroundColor Green
