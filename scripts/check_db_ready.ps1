[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$VenvPath = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
$BackendPath = Join-Path $ProjectRoot "backend"
$BackendEnv = Join-Path $BackendPath ".env"
$ResultCode = 0

Write-Host "OutcomeIQ database readiness check" -ForegroundColor Cyan

try {
    Set-Location $ProjectRoot

    if (-not (Test-Path -LiteralPath $VenvPath -PathType Container)) {
        Write-Host "DATABASE ERROR" -ForegroundColor Red
        Write-Host "Virtual environment not found at $VenvPath" -ForegroundColor Yellow
        $ResultCode = 1
    }
    elseif (-not (Test-Path -LiteralPath $VenvPython -PathType Leaf)) {
        Write-Host "DATABASE ERROR" -ForegroundColor Red
        Write-Host "Virtual-environment Python executable is missing." -ForegroundColor Yellow
        $ResultCode = 1
    }
    elseif (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
        Write-Host "DATABASE ERROR" -ForegroundColor Red
        Write-Host "Virtual-environment activation script is missing." -ForegroundColor Yellow
        $ResultCode = 1
    }
    elseif (-not (Test-Path -LiteralPath $BackendPath -PathType Container)) {
        Write-Host "DATABASE ERROR" -ForegroundColor Red
        Write-Host "Backend folder not found at $BackendPath" -ForegroundColor Yellow
        $ResultCode = 1
    }
    elseif (-not (Test-Path -LiteralPath $BackendEnv -PathType Leaf)) {
        Write-Host "DATABASE NOT CONFIGURED" -ForegroundColor Yellow
        Write-Host "Create backend\.env from backend\.env.example, then set DATABASE_URL." -ForegroundColor Yellow
        $ResultCode = 0
    }
    else {
        . $ActivateScript
        Set-Location $BackendPath

        python -m scripts.check_db_connection
        $ResultCode = $LASTEXITCODE
    }
}
catch {
    Write-Host "DATABASE ERROR" -ForegroundColor Red
    Write-Host "The readiness script could not complete. Verify the project files and virtual environment." -ForegroundColor Yellow
    $ResultCode = 1
}
finally {
    Set-Location $OriginalLocation
}

exit $ResultCode
