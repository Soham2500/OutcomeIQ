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
    @{ Label = "Database session foundation"; RelativePath = "backend\app\db\session.py" },
    @{ Label = "SQLAlchemy declarative base"; RelativePath = "backend\app\db\base.py" },
    @{ Label = "SQLAlchemy database mixins"; RelativePath = "backend\app\db\mixins.py" },
    @{ Label = "Database health helper"; RelativePath = "backend\app\db\health.py" },
    @{ Label = "System metadata model"; RelativePath = "backend\app\models\system.py" },
    @{ Label = "Core model enums"; RelativePath = "backend\app\models\enums.py" },
    @{ Label = "User model"; RelativePath = "backend\app\models\user.py" },
    @{ Label = "Organization model"; RelativePath = "backend\app\models\organization.py" },
    @{ Label = "Project model"; RelativePath = "backend\app\models\project.py" },
    @{ Label = "Project member model"; RelativePath = "backend\app\models\project_member.py" },
    @{ Label = "Audit event model"; RelativePath = "backend\app\models\audit_event.py" },
    @{ Label = "Alembic configuration"; RelativePath = "backend\alembic.ini" },
    @{ Label = "Alembic environment"; RelativePath = "backend\alembic\env.py" },
    @{ Label = "Alembic revision template"; RelativePath = "backend\alembic\script.py.mako" },
    @{ Label = "Alembic versions placeholder"; RelativePath = "backend\alembic\versions\.gitkeep" },
    @{ Label = "Backend requirements"; RelativePath = "backend\requirements.txt" },
    @{ Label = "Backend .env.example"; RelativePath = "backend\.env.example" },
    @{ Label = "Health tests"; RelativePath = "backend\tests\test_health.py" },
    @{ Label = "System metadata model tests"; RelativePath = "backend\tests\test_system_model.py" },
    @{ Label = "Core model tests"; RelativePath = "backend\tests\test_models.py" },
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
    @{ Label = "Docker check script"; RelativePath = "scripts\check_docker.ps1" },
    @{ Label = "Database readiness script"; RelativePath = "scripts\check_db_ready.ps1" },
    @{ Label = "Database migration script"; RelativePath = "scripts\db_migrate.ps1" },
    @{ Label = "Database current revision script"; RelativePath = "scripts\db_current.ps1" },
    @{ Label = "Database history script"; RelativePath = "scripts\db_history.ps1" },
    @{ Label = "Database table check script"; RelativePath = "scripts\check_db_tables.ps1" },
    @{ Label = "Day 3 local environment guide"; RelativePath = "docs\day-3-local-env-setup.md" },
    @{ Label = "Day 3 environment template"; RelativePath = "docs\day-3-env-template.md" },
    @{ Label = "Local PostgreSQL guide"; RelativePath = "docs\postgresql-local-setup.md" },
    @{ Label = "Database readiness Python helper"; RelativePath = "backend\scripts\check_db_connection.py" },
    @{ Label = "Database table check Python helper"; RelativePath = "backend\scripts\check_db_tables.py" },
    @{ Label = "Day 3 Alembic migration guide"; RelativePath = "docs\day-3-alembic-migration.md" },
    @{ Label = "Day 3 core database model guide"; RelativePath = "docs\day-3-core-database-models.md" },
    @{ Label = "Core identity/project migration"; RelativePath = "backend\alembic\versions\20260704_0002_create_core_identity_project_tables.py" },
    @{ Label = "Local database creation SQL helper"; RelativePath = "database\local\create_outcomeiq_dev.sql" }
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

$MigrationPath = Join-Path $ProjectRoot "backend\alembic\versions"
$MigrationFiles = @(
    Get-ChildItem -LiteralPath $MigrationPath -Filter "*.py" -File -ErrorAction SilentlyContinue
)
if ($MigrationFiles.Count -ge 1) {
    Write-Host "$FoundMark Alembic migration revision" -ForegroundColor Green
}
else {
    Write-Host "$MissingMark Alembic migration revision - no Python revision found in $MigrationPath" -ForegroundColor Red
    $AllChecksPassed = $false
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
