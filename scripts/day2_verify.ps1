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
    @{ Label = "Authentication security utilities"; RelativePath = "backend\app\core\security.py" },
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
    @{ Label = "User schemas"; RelativePath = "backend\app\schemas\user.py" },
    @{ Label = "Organization schemas"; RelativePath = "backend\app\schemas\organization.py" },
    @{ Label = "Project schemas"; RelativePath = "backend\app\schemas\project.py" },
    @{ Label = "Project member schemas"; RelativePath = "backend\app\schemas\project_member.py" },
    @{ Label = "Audit event schemas"; RelativePath = "backend\app\schemas\audit_event.py" },
    @{ Label = "Authentication schemas"; RelativePath = "backend\app\schemas\auth.py" },
    @{ Label = "User repository"; RelativePath = "backend\app\repositories\user_repository.py" },
    @{ Label = "Organization repository"; RelativePath = "backend\app\repositories\organization_repository.py" },
    @{ Label = "Project repository"; RelativePath = "backend\app\repositories\project_repository.py" },
    @{ Label = "Project member repository"; RelativePath = "backend\app\repositories\project_member_repository.py" },
    @{ Label = "Audit repository"; RelativePath = "backend\app\repositories\audit_repository.py" },
    @{ Label = "Development seed service"; RelativePath = "backend\app\services\dev_seed_service.py" },
    @{ Label = "Authentication service"; RelativePath = "backend\app\services\auth_service.py" },
    @{ Label = "Audit service"; RelativePath = "backend\app\services\audit_service.py" },
    @{ Label = "Authentication API endpoints"; RelativePath = "backend\app\api\v1\endpoints\auth.py" },
    @{ Label = "Organization API endpoints"; RelativePath = "backend\app\api\v1\endpoints\organizations.py" },
    @{ Label = "Project API endpoints"; RelativePath = "backend\app\api\v1\endpoints\projects.py" },
    @{ Label = "Authentication API dependency"; RelativePath = "backend\app\api\dependencies.py" },
    @{ Label = "Alembic configuration"; RelativePath = "backend\alembic.ini" },
    @{ Label = "Alembic environment"; RelativePath = "backend\alembic\env.py" },
    @{ Label = "Alembic revision template"; RelativePath = "backend\alembic\script.py.mako" },
    @{ Label = "Alembic versions placeholder"; RelativePath = "backend\alembic\versions\.gitkeep" },
    @{ Label = "Backend requirements"; RelativePath = "backend\requirements.txt" },
    @{ Label = "Backend .env.example"; RelativePath = "backend\.env.example" },
    @{ Label = "Health tests"; RelativePath = "backend\tests\test_health.py" },
    @{ Label = "System metadata model tests"; RelativePath = "backend\tests\test_system_model.py" },
    @{ Label = "Core model tests"; RelativePath = "backend\tests\test_models.py" },
    @{ Label = "Schema tests"; RelativePath = "backend\tests\test_schemas.py" },
    @{ Label = "Repository import tests"; RelativePath = "backend\tests\test_repositories_imports.py" },
    @{ Label = "Development seed import tests"; RelativePath = "backend\tests\test_dev_seed_imports.py" },
    @{ Label = "Database script import tests"; RelativePath = "backend\tests\test_database_scripts_imports.py" },
    @{ Label = "Security tests"; RelativePath = "backend\tests\test_security.py" },
    @{ Label = "Authentication schema tests"; RelativePath = "backend\tests\test_auth_schemas.py" },
    @{ Label = "Authentication import tests"; RelativePath = "backend\tests\test_auth_imports.py" },
    @{ Label = "Organization/project import tests"; RelativePath = "backend\tests\test_organization_project_imports.py" },
    @{ Label = "Organization/project schema tests"; RelativePath = "backend\tests\test_organization_project_schemas.py" },
    @{ Label = "API dependency import tests"; RelativePath = "backend\tests\test_api_dependencies_imports.py" },
    @{ Label = "Audit service import tests"; RelativePath = "backend\tests\test_audit_service_imports.py" },
    @{ Label = "Route registration tests"; RelativePath = "backend\tests\test_route_registration.py" },
    @{ Label = "Day 4 final import tests"; RelativePath = "backend\tests\test_day4_final_imports.py" },
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
    @{ Label = "Auth/project API smoke script"; RelativePath = "scripts\smoke_auth_project_api.ps1" },
    @{ Label = "Docker check script"; RelativePath = "scripts\check_docker.ps1" },
    @{ Label = "Database readiness script"; RelativePath = "scripts\check_db_ready.ps1" },
    @{ Label = "Database migration script"; RelativePath = "scripts\db_migrate.ps1" },
    @{ Label = "Database current revision script"; RelativePath = "scripts\db_current.ps1" },
    @{ Label = "Database history script"; RelativePath = "scripts\db_history.ps1" },
    @{ Label = "Database table check script"; RelativePath = "scripts\check_db_tables.ps1" },
    @{ Label = "Development seed PowerShell script"; RelativePath = "scripts\db_seed_dev.ps1" },
    @{ Label = "Core data check PowerShell script"; RelativePath = "scripts\check_core_data.ps1" },
    @{ Label = "Database schema inspection PowerShell script"; RelativePath = "scripts\inspect_db_schema.ps1" },
    @{ Label = "Alembic validation PowerShell script"; RelativePath = "scripts\validate_alembic_state.ps1" },
    @{ Label = "Day 3 local environment guide"; RelativePath = "docs\day-3-local-env-setup.md" },
    @{ Label = "Day 3 environment template"; RelativePath = "docs\day-3-env-template.md" },
    @{ Label = "Local PostgreSQL guide"; RelativePath = "docs\postgresql-local-setup.md" },
    @{ Label = "Database readiness Python helper"; RelativePath = "backend\scripts\check_db_connection.py" },
    @{ Label = "Database table check Python helper"; RelativePath = "backend\scripts\check_db_tables.py" },
    @{ Label = "Development seed Python helper"; RelativePath = "backend\scripts\seed_dev_data.py" },
    @{ Label = "Core data check Python helper"; RelativePath = "backend\scripts\check_core_data.py" },
    @{ Label = "Database schema inspection Python helper"; RelativePath = "backend\scripts\inspect_db_schema.py" },
    @{ Label = "Alembic validation Python helper"; RelativePath = "backend\scripts\validate_alembic_state.py" },
    @{ Label = "Day 3 Alembic migration guide"; RelativePath = "docs\day-3-alembic-migration.md" },
    @{ Label = "Day 3 core database model guide"; RelativePath = "docs\day-3-core-database-models.md" },
    @{ Label = "Day 3 core data access guide"; RelativePath = "docs\day-3-core-data-access-layer.md" },
    @{ Label = "Day 3 final summary"; RelativePath = "docs\day-3-final-summary.md" },
    @{ Label = "Day 4 auth readiness checklist"; RelativePath = "docs\day-4-auth-readiness.md" },
    @{ Label = "Day 4 starter prompt"; RelativePath = "docs\day-4-start-prompt.md" },
    @{ Label = "Day 4 authentication testing guide"; RelativePath = "docs\day-4-auth-testing.md" },
    @{ Label = "Day 4 checkpoint"; RelativePath = "docs\day-4-checkpoint.md" },
    @{ Label = "Day 4 organization/project API guide"; RelativePath = "docs\day-4-organization-project-apis.md" },
    @{ Label = "Day 4 manual API testing guide"; RelativePath = "docs\day-4-manual-api-testing.md" },
    @{ Label = "Day 4 API smoke testing guide"; RelativePath = "docs\day-4-api-smoke-testing.md" },
    @{ Label = "Day 4 final summary"; RelativePath = "docs\day-4-final-summary.md" },
    @{ Label = "Day 5 workflow logging plan"; RelativePath = "docs\day-5-workflow-logging-plan.md" },
    @{ Label = "Day 5 starter prompt"; RelativePath = "docs\day-5-start-prompt.md" },
    @{ Label = "Workflow model"; RelativePath = "backend\app\models\workflow.py" },
    @{ Label = "Workflow configuration model"; RelativePath = "backend\app\models\workflow_configuration.py" },
    @{ Label = "Workflow run model"; RelativePath = "backend\app\models\workflow_run.py" },
    @{ Label = "Model call model"; RelativePath = "backend\app\models\model_call.py" },
    @{ Label = "Tool call model"; RelativePath = "backend\app\models\tool_call.py" },
    @{ Label = "Workflow model tests"; RelativePath = "backend\tests\test_workflow_models.py" },
    @{ Label = "Day 5 workflow database model guide"; RelativePath = "docs\day-5-workflow-database-models.md" },
    @{ Label = "Day 5 checkpoint"; RelativePath = "docs\day-5-checkpoint.md" },
    @{ Label = "Workflow schemas"; RelativePath = "backend\app\schemas\workflow.py" },
    @{ Label = "Workflow configuration schemas"; RelativePath = "backend\app\schemas\workflow_configuration.py" },
    @{ Label = "Workflow run schemas"; RelativePath = "backend\app\schemas\workflow_run.py" },
    @{ Label = "Model call schemas"; RelativePath = "backend\app\schemas\model_call.py" },
    @{ Label = "Tool call schemas"; RelativePath = "backend\app\schemas\tool_call.py" },
    @{ Label = "Workflow repository"; RelativePath = "backend\app\repositories\workflow_repository.py" },
    @{ Label = "Workflow configuration repository"; RelativePath = "backend\app\repositories\workflow_configuration_repository.py" },
    @{ Label = "Workflow run repository"; RelativePath = "backend\app\repositories\workflow_run_repository.py" },
    @{ Label = "Model call repository"; RelativePath = "backend\app\repositories\model_call_repository.py" },
    @{ Label = "Tool call repository"; RelativePath = "backend\app\repositories\tool_call_repository.py" },
    @{ Label = "Workflow logging service"; RelativePath = "backend\app\services\workflow_logging_service.py" },
    @{ Label = "Workflow API endpoints"; RelativePath = "backend\app\api\v1\endpoints\workflows.py" },
    @{ Label = "Workflow run API endpoints"; RelativePath = "backend\app\api\v1\endpoints\workflow_runs.py" },
    @{ Label = "Workflow API smoke script"; RelativePath = "scripts\smoke_workflow_logging_api.ps1" },
    @{ Label = "Workflow schema tests"; RelativePath = "backend\tests\test_workflow_schemas.py" },
    @{ Label = "Workflow repository import tests"; RelativePath = "backend\tests\test_workflow_repositories_imports.py" },
    @{ Label = "Workflow service import tests"; RelativePath = "backend\tests\test_workflow_service_imports.py" },
    @{ Label = "Workflow route registration tests"; RelativePath = "backend\tests\test_workflow_route_registration.py" },
    @{ Label = "Day 5 workflow API guide"; RelativePath = "docs\day-5-workflow-logging-apis.md" },
    @{ Label = "Core identity/project migration"; RelativePath = "backend\alembic\versions\20260704_0002_create_core_identity_project_tables.py" },
    @{ Label = "Workflow logging migration"; RelativePath = "backend\alembic\versions\20260704_0003_create_workflow_logging_tables.py" },
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
