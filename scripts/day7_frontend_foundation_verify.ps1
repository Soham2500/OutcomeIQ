[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FrontendPath = Join-Path $ProjectRoot "frontend"
$PowerShellExecutable = (Get-Process -Id $PID).Path
$CurrentStep = "initialization"
$Succeeded = $false

function Invoke-RepositoryScript {
    param([string]$RelativePath)

    & $PowerShellExecutable `
        -NoProfile `
        -ExecutionPolicy Bypass `
        -File (Join-Path $ProjectRoot $RelativePath)
    if ($LASTEXITCODE -ne 0) {
        throw "$RelativePath failed with exit code $LASTEXITCODE."
    }
}

Write-Host "OutcomeIQ Day 7 frontend foundation verification" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "backend environment Git protection"
    git check-ignore -q -- "backend/.env"
    if ($LASTEXITCODE -ne 0) {
        throw "backend/.env is not protected by a Git ignore rule."
    }
    $EnvironmentStatus = @(
        git status --short --untracked-files=all |
            Where-Object { $_ -match '(^|\s)backend[\\/]\.env$' }
    )
    if ($EnvironmentStatus.Count -gt 0) {
        throw "backend/.env appears in Git status. Stop and protect the file."
    }

    $CurrentStep = "frontend structure"
    if (-not (Test-Path -LiteralPath $FrontendPath -PathType Container)) {
        throw "The frontend folder was not found."
    }
    if (-not (Test-Path -LiteralPath (Join-Path $FrontendPath "package.json") -PathType Leaf)) {
        throw "frontend\package.json was not found."
    }

    $CurrentStep = "frontend dependency installation"
    Invoke-RepositoryScript "scripts\install_frontend.ps1"

    $CurrentStep = "frontend typecheck"
    Invoke-RepositoryScript "scripts\frontend_typecheck.ps1"

    $Succeeded = $true
}
catch {
    Write-Host "DAY 7 FRONTEND FOUNDATION VERIFY FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "DAY 7 FRONTEND FOUNDATION VERIFY PASSED" -ForegroundColor Green
    exit 0
}

exit 1
