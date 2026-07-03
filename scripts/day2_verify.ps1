[CmdletBinding()]
param()

$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$BackendPath = Join-Path $ProjectRoot "backend"
$FoundMark = [char]0x2705
$MissingMark = [char]0x274C
$AllChecksPassed = $true

Write-Host "OutcomeIQ Day 2 verification" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"
Set-Location $ProjectRoot

$RequiredPaths = @(
    @{ Label = "Product understanding document"; RelativePath = "docs\product-understanding.md" },
    @{ Label = "MVP scope document"; RelativePath = "docs\mvp-scope.md" },
    @{ Label = "System architecture document"; RelativePath = "docs\system-architecture.md" },
    @{ Label = "Database design document"; RelativePath = "docs\database-design.md" },
    @{ Label = "API design document"; RelativePath = "docs\api-design.md" },
    @{ Label = "Day 2 final summary"; RelativePath = "docs\day-2-final-summary.md" },
    @{ Label = "Day 3 database setup plan"; RelativePath = "docs\day-3-database-setup-plan.md" },
    @{ Label = "FastAPI main module"; RelativePath = "backend\app\main.py" },
    @{ Label = "API v1 router"; RelativePath = "backend\app\api\v1\router.py" },
    @{ Label = "Health endpoints"; RelativePath = "backend\app\api\v1\endpoints\health.py" },
    @{ Label = "Core configuration"; RelativePath = "backend\app\core\config.py" },
    @{ Label = "Structured logging"; RelativePath = "backend\app\core\logging.py" },
    @{ Label = "Database session placeholder"; RelativePath = "backend\app\db\session.py" },
    @{ Label = "Backend requirements"; RelativePath = "backend\requirements.txt" },
    @{ Label = "Backend .env.example"; RelativePath = "backend\.env.example" },
    @{ Label = "Health tests"; RelativePath = "backend\tests\test_health.py" },
    @{ Label = "Backend README"; RelativePath = "backend\README.md" },
    @{ Label = "Root .gitignore"; RelativePath = ".gitignore" },
    @{ Label = "Root .gitattributes"; RelativePath = ".gitattributes" },
    @{ Label = "Root .editorconfig"; RelativePath = ".editorconfig" },
    @{ Label = "Root README"; RelativePath = "README.md" },
    @{ Label = "Application constants"; RelativePath = "backend\app\core\constants.py" },
    @{ Label = "Backend run script"; RelativePath = "scripts\run_backend.ps1" },
    @{ Label = "Backend test script"; RelativePath = "scripts\test_backend.ps1" },
    @{ Label = "Backend check script"; RelativePath = "scripts\check_backend.ps1" },
    @{ Label = "API smoke script"; RelativePath = "scripts\smoke_api.ps1" },
    @{ Label = "Docker check script"; RelativePath = "scripts\check_docker.ps1" }
)

foreach ($Required in $RequiredPaths) {
    $FullPath = Join-Path $ProjectRoot $Required.RelativePath
    if (Test-Path -LiteralPath $FullPath -PathType Leaf) {
        Write-Host "$FoundMark $($Required.Label)" -ForegroundColor Green
    }
    else {
        Write-Host "$MissingMark $($Required.Label) - missing: $FullPath" -ForegroundColor Red
        $AllChecksPassed = $false
    }
}

$VenvPath = Join-Path $ProjectRoot ".venv"
if (Test-Path -LiteralPath $VenvPath -PathType Container) {
    Write-Host "$FoundMark .venv folder" -ForegroundColor Green
}
else {
    Write-Host "$MissingMark .venv folder - missing: $VenvPath" -ForegroundColor Red
    $AllChecksPassed = $false
}

if (Test-Path -LiteralPath $VenvPython -PathType Leaf) {
    Write-Host "$FoundMark .venv Python executable" -ForegroundColor Green
}
else {
    Write-Host "$MissingMark .venv Python executable - missing: $VenvPython" -ForegroundColor Red
    $AllChecksPassed = $false
}

$CanRunTests = (Test-Path -LiteralPath $VenvPython -PathType Leaf) -and (Test-Path -LiteralPath $BackendPath -PathType Container)
if ($CanRunTests) {
    Write-Host "Running backend tests..." -ForegroundColor Cyan
    Push-Location $BackendPath
    try {
        & $VenvPython -m pytest -v
        if ($LASTEXITCODE -eq 0) {
            Write-Host "$FoundMark Backend tests passed" -ForegroundColor Green
        }
        else {
            Write-Host "$MissingMark Backend tests failed with exit code $LASTEXITCODE" -ForegroundColor Red
            $AllChecksPassed = $false
        }
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "$MissingMark Backend tests could not run because the environment or backend folder is missing." -ForegroundColor Red
    $AllChecksPassed = $false
}

if ($AllChecksPassed) {
    Write-Host "DAY 2 CHECK PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "DAY 2 CHECK FAILED" -ForegroundColor Red
exit 1
