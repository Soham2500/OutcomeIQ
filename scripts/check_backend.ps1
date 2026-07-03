[CmdletBinding()]
param()

$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$FoundMark = [char]0x2705
$MissingMark = [char]0x274C
$WarningMark = "$([char]0x26A0)$([char]0xFE0F)"
$AllRequiredFound = $true

Write-Host "OutcomeIQ backend structure check" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"

$RequiredChecks = @(
    @{ Label = "Project root"; Path = $ProjectRoot; Type = "Container" },
    @{ Label = ".venv folder"; Path = (Join-Path $ProjectRoot ".venv"); Type = "Container" },
    @{ Label = ".venv Python executable"; Path = (Join-Path $ProjectRoot ".venv\Scripts\python.exe"); Type = "Leaf" },
    @{ Label = "Backend folder"; Path = (Join-Path $ProjectRoot "backend"); Type = "Container" },
    @{ Label = "Backend requirements"; Path = (Join-Path $ProjectRoot "backend\requirements.txt"); Type = "Leaf" },
    @{ Label = "FastAPI main module"; Path = (Join-Path $ProjectRoot "backend\app\main.py"); Type = "Leaf" },
    @{ Label = "API v1 router"; Path = (Join-Path $ProjectRoot "backend\app\api\v1\router.py"); Type = "Leaf" },
    @{ Label = "Health endpoints"; Path = (Join-Path $ProjectRoot "backend\app\api\v1\endpoints\health.py"); Type = "Leaf" },
    @{ Label = "Health tests"; Path = (Join-Path $ProjectRoot "backend\tests\test_health.py"); Type = "Leaf" },
    @{ Label = "Backend .env.example"; Path = (Join-Path $ProjectRoot "backend\.env.example"); Type = "Leaf" },
    @{ Label = "Backend README"; Path = (Join-Path $ProjectRoot "backend\README.md"); Type = "Leaf" },
    @{ Label = "Root README"; Path = (Join-Path $ProjectRoot "README.md"); Type = "Leaf" },
    @{ Label = "Root .gitignore"; Path = (Join-Path $ProjectRoot ".gitignore"); Type = "Leaf" },
    @{ Label = "Documentation folder"; Path = (Join-Path $ProjectRoot "docs"); Type = "Container" }
)

foreach ($Check in $RequiredChecks) {
    if (Test-Path -LiteralPath $Check.Path -PathType $Check.Type) {
        Write-Host "$FoundMark $($Check.Label)" -ForegroundColor Green
    }
    else {
        Write-Host "$MissingMark $($Check.Label) - missing: $($Check.Path)" -ForegroundColor Red
        $AllRequiredFound = $false
    }
}

$LocalEnvPath = Join-Path $ProjectRoot "backend\.env"
if (Test-Path -LiteralPath $LocalEnvPath -PathType Leaf) {
    Write-Host "$WarningMark Optional local backend .env exists and should remain uncommitted." -ForegroundColor Yellow
}
else {
    Write-Host "$WarningMark Optional local backend .env is not present; .env.example is sufficient for source control." -ForegroundColor Yellow
}

Write-Host "$WarningMark PostgreSQL, authentication, and frontend are future milestones and are not checked." -ForegroundColor Yellow

if ($AllRequiredFound) {
    Write-Host "Backend structure check passed." -ForegroundColor Green
    exit 0
}

Write-Host "Backend structure check failed." -ForegroundColor Red
exit 1
