# OutcomeIQ Backend

Initial FastAPI modular-monolith foundation for the OutcomeIQ outcome-aware AI FinOps platform.

## Current status

**Day 2, Day 3 and Day 4 are complete. Day 5 has started.** Authentication and the organization/project MVP API foundation are verified. Five workflow logging models and an unapplied migration are now prepared.

Available now:

- FastAPI application setup
- Versioned API router
- Root, health and readiness endpoints
- Environment-backed settings
- Configurable CORS origins
- Structured JSON logging
- SQLAlchemy declarative base with approved infrastructure and core models
- Conditional engine and session factory when `DATABASE_URL` is present
- Safe database readiness check using `SELECT 1`
- Alembic environment with approved core and workflow models registered
- First infrastructure migration for `system_metadata`
- Applied core migration for users, organizations, projects, memberships and audit events
- Pydantic schemas and SQLAlchemy repositories for core records
- Explicit, idempotent local development seed tooling
- Read-only schema inspection and Alembic-state validation
- Bcrypt password hashing and JWT access-token utilities
- Register, login and protected current-user endpoints
- Authenticated organization/project CRUD endpoints with audit events
- Automatic owner membership for newly created projects
- Membership-scoped project listing/read access and owner/admin updates
- Safe shared audit service and live auth/project API smoke test
- Workflow, workflow-configuration, run, model-call and tool-call models
- Unapplied `0003_workflow_logging` Alembic revision
- Endpoint, model and access-layer tests
- Docker packaging

Not implemented yet:

- Advanced authentication such as refresh tokens, reset, MFA or SSO
- Workflow, cost, outcome and recommendation APIs
- Outcome, cost-summary and recommendation models/tables
- Workflow repositories and HTTP APIs
- Redis integration
- Frontend code

## Prerequisites

- Python 3.11 or newer; Python 3.12 is recommended
- `pip`
- Docker Desktop only if using Docker

## Developer scripts

The repository provides PowerShell helpers. Run them from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_backend.ps1
.\scripts\test_backend.ps1
.\scripts\day2_verify.ps1
.\scripts\run_backend.ps1
.\scripts\smoke_api.ps1
.\scripts\check_docker.ps1
.\scripts\check_db_ready.ps1
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

- `check_backend.ps1` verifies the expected structure without changing anything.
- `test_backend.ps1` activates `.venv` and runs pytest.
- `day2_verify.ps1` checks all Day 1/2 deliverables and runs tests.
- `run_backend.ps1` activates `.venv` and starts Uvicorn with auto-reload.
- `smoke_api.ps1` checks the three running API endpoints from another terminal.
- `check_docker.ps1` reports Docker and Compose availability without starting anything.
- `check_db_ready.ps1` reports database configuration/connectivity without creating databases, tables or migrations.
- `db_seed_dev.ps1` explicitly inserts only the safe demo identity/project records.
- `check_core_data.ps1` reports core row counts and demo-data presence without changing data.
- `inspect_db_schema.ps1` lists safe table and column metadata without changing data.
- `validate_alembic_state.ps1` confirms migration files and the current database head without running migrations.
- `db_history.ps1` and `db_current.ps1` inspect Alembic state.
- `db_migrate.ps1` explicitly applies reviewed migrations through `alembic upgrade head`.
- `check_db_tables.ps1` safely checks all required core and workflow tables.

## Setup on Windows PowerShell

Open PowerShell and begin at the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
```

Create the root virtual environment:

```powershell
python -m venv .venv
```

Allow activation scripts for the current PowerShell process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

Move into the backend directory:

```powershell
cd backend
```

Create a local environment file if one does not already exist:

```powershell
Copy-Item .env.example .env
```

No PostgreSQL or Redis URL is required for FastAPI startup. An empty `DATABASE_URL` reports `not_configured`.

## Run the FastAPI server

From the `backend` directory with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Readiness: `http://127.0.0.1:8000/api/v1/ready`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Available endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Basic service discovery |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Dependency readiness; database is `not_configured`, `connected` or `error` |
| POST | `/api/v1/auth/register` | Register a user without exposing the password hash |
| POST | `/api/v1/auth/login` | Return a bearer access token |
| GET | `/api/v1/auth/me` | Return the authenticated active user |
| POST/GET | `/api/v1/organizations` | Create or list organizations |
| GET/PATCH | `/api/v1/organizations/{organization_id}` | Read or update an organization |
| POST/GET | `/api/v1/projects` | Create or list projects |
| GET/PATCH | `/api/v1/projects/{project_id}` | Read or update a project |
| GET | `/api/v1/projects/{project_id}/members` | List project memberships |
| GET | `/docs` | Swagger UI |

## Stop the server

Press `Ctrl+C` in the PowerShell window running Uvicorn.

## Run the smoke API check

Keep Uvicorn running in the first PowerShell window. Open a second PowerShell window and run from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\smoke_api.ps1
```

The smoke script reports a helpful failure if the API is not running; it never launches Uvicorn itself.

## Run tests

From the `backend` directory:

```powershell
python -m pytest -v
```

Expected result:

```text
28 passed
```

Run only the health tests when needed:

```powershell
python -m pytest tests\test_health.py -v
```

The pytest configuration intentionally leaves warnings visible.

The current `StarletteDeprecationWarning` related to FastAPI TestClient and HTTPX is non-blocking. It does not change the `28 passed` result and should remain visible until the upstream compatibility path is addressed deliberately.

## Verified commands

From the project root:

```powershell
.\scripts\day2_verify.ps1
.\scripts\test_backend.ps1
.\scripts\run_backend.ps1
```

With the API running in the first window, use a second PowerShell window:

```powershell
.\scripts\smoke_api.ps1
```

Verified results are twenty-eight passing tests, including isolated auth flow, authorization behavior, audit-redaction, route, Day 4 closure and workflow-model metadata checks.

## Run with Docker

Docker Desktop must be installed and running.

From the `backend` directory:

```powershell
docker compose up --build
```

Check the health endpoint:

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/health
```

Stop and remove the backend container:

```powershell
docker compose down
```

The Compose file intentionally contains only the backend service. PostgreSQL and Redis are deferred.

## Configuration

Settings load from environment variables or `backend\.env`. Available values are documented in `.env.example`.

Current optional placeholders:

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`

Do not use the example JWT secret in a deployed environment.

## Database foundation

Create `backend\.env` manually from the safe example if needed:

```powershell
Copy-Item .env.example .env
```

Set the private local value using this format:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `YOUR_PASSWORD` locally. Never commit or print the completed URL.

From the project root, check status with:

```powershell
.\scripts\check_db_ready.ps1
```

The result is one of:

- `DATABASE NOT CONFIGURED` before `.env`/URL setup; acceptable in early Day 3
- `DATABASE CONNECTED` after PostgreSQL and credentials are correct
- `DATABASE ERROR` when configured connectivity fails or the script cannot complete

The check performs only `SELECT 1`. It never creates a database, table or migration.

## First Alembic infrastructure migration

Alembic uses the private `DATABASE_URL` from application settings and `Base.metadata` from `app/db/base.py`. Metadata now contains `SystemMetadata` plus the approved user, organization, project, project-membership and audit-event models.

From the project root, inspect migration state with:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
```

Apply any pending reviewed migration explicitly, then verify the table:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

Revisions `0001_system_metadata` and `0002_core_identity_projects` are applied. Revision `0003_workflow_logging` is prepared but intentionally unapplied. Before applying it, the table checker lists the five workflow tables as missing; afterward it reports `ALL REQUIRED TABLES EXIST`. See `docs/day-5-workflow-database-models.md` for boundaries and commands.

## Development seed and core data check

The seed is never run at application startup. Invoke it explicitly from the project root:

```powershell
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
```

The verified local seed contains one user, organization, project, project membership and audit event. The checker reports `CORE DEVELOPMENT DATA FOUND`.

## Day 3 database foundation complete

Run the final read-only database checks from the project root:

```powershell
.\scripts\check_db_ready.ps1
.\scripts\check_db_tables.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
```

Expected key results are `DATABASE CONNECTED`, `ALL CORE TABLES EXIST`, `CORE DEVELOPMENT DATA FOUND` and `ALEMBIC STATE VALID`.

## Day 4 authentication foundation

Install the declared authentication dependencies from the project root:

```powershell
pip install -r backend\requirements.txt
```

Run the backend, open `http://127.0.0.1:8000/docs`, register a synthetic user, log in, copy the returned access token, select Swagger's **Authorize** button, and call `/api/v1/auth/me`.

After authorization, create an organization, create a project with the returned organization ID, list projects and inspect `/api/v1/projects/{project_id}/members`. The project creator should have role `owner`. See `docs/day-4-manual-api-testing.md` for the complete sequence.

With the backend already running and PostgreSQL connected, run the live local smoke path from another PowerShell window:

```powershell
.\scripts\smoke_auth_project_api.ps1
```

This creates timestamped synthetic local data. It does not start the server, run migrations, delete rows or print the password/access token.

`backend/.env` must remain ignored. Never hardcode or print `JWT_SECRET_KEY`, and never expose `hashed_password` through an API schema or response.

## Troubleshooting

### PowerShell blocks virtual-environment activation

Run this in the same PowerShell window, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run these commands from the project root. If already inside `backend`, return to the root first with `cd ..`.

### `python` is not recognized

Try the Windows Python launcher:

```powershell
py -m venv .venv
```

If neither `python` nor `py` works, reinstall Python and select **Add Python to PATH**.

### `ModuleNotFoundError: app`

Confirm Uvicorn and pytest are running from:

```text
C:\Users\soham\OneDrive\Documents\pro\backend
```

Also confirm the root virtual environment is active.

### `ModuleNotFoundError: fastapi`

Activate the virtual environment and reinstall dependencies from the project root:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Port 8000 is already in use

Use a different port:

```powershell
uvicorn app.main:app --reload --port 8001
```

### Swagger UI does not open

Confirm Uvicorn shows a successful startup and open `http://127.0.0.1:8000/docs`, not the filesystem path.

### Docker cannot start

Confirm Docker Desktop is running and configured for Linux containers.

## Day 5 workflow logging foundation

The live Day 4 smoke result is `AUTH PROJECT API SMOKE CHECK PASSED`. Day 5 now defines `workflows`, `workflow_configurations`, `workflow_runs`, `model_calls` and `tool_calls` without applying the migration automatically.

After reviewing the migration, apply and verify it from the project root:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

The next milestone is repositories and a simulated workflow logging API. Real provider integrations, outcomes, cost attribution, recommendations and frontend work remain deferred.
