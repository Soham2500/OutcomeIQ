[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
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

Write-Host "OutcomeIQ Day 8 frontend polish verification" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    $CurrentStep = "private environment Git protection"
    foreach ($EnvironmentPath in @("backend/.env", "frontend/.env")) {
        git check-ignore -q -- $EnvironmentPath
        if ($LASTEXITCODE -ne 0) {
            throw "$EnvironmentPath is not protected by a Git ignore rule."
        }
    }
    $EnvironmentStatus = @(
        git status --short --untracked-files=all |
            Where-Object {
                $_ -match '(^|\s)(backend|frontend)[\\/]\.env$'
            }
    )
    if ($EnvironmentStatus.Count -gt 0) {
        throw "A private environment file appears in Git status."
    }

    $CurrentStep = "Day 8 frontend file checks"
    $RequiredPaths = @(
        "frontend\src\pages\DemoGuidePage.tsx",
        "frontend\src\components\AppLogo.tsx",
        "frontend\src\utils\format.ts"
    )
    foreach ($RelativePath in $RequiredPaths) {
        if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $RelativePath) -PathType Leaf)) {
            throw "Required Day 8 file is missing: $RelativePath"
        }
    }

    $CurrentStep = "frontend dependency installation"
    Invoke-RepositoryScript "scripts\install_frontend.ps1"

    $CurrentStep = "frontend typecheck"
    Invoke-RepositoryScript "scripts\frontend_typecheck.ps1"

    $Succeeded = $true
}
catch {
    Write-Host "DAY 8 FRONTEND POLISH VERIFY FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
}
finally {
    Set-Location $OriginalLocation
}

if ($Succeeded) {
    Write-Host "DAY 8 FRONTEND POLISH VERIFY PASSED" -ForegroundColor Green
    exit 0
}

exit 1
